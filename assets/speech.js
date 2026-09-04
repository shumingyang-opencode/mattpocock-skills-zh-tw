/* speech.js — L3 語音朗讀核心邏輯（智慧跟讀 + 段落高亮 + 中英切換） */

(function () {
  "use strict";

  /* ============================================================
   *  工具函式
   * ============================================================ */

  /** 判斷字串是否以中文字符為主 */
  function isMostlyChinese(text) {
    const m = text.match(/[\u4e00-\u9fff\u3400-\u4dbf]/g);
    return m ? m.length / text.length > 0.3 : false;
  }

  /** 從 nodes 提取純文字（跳過 hidden / script / style） */
  function nodeText(node) {
    if (node.nodeType === Node.TEXT_NODE) return node.textContent;
    if (node.nodeType !== Node.ELEMENT_NODE) return "";
    const tag = node.tagName.toLowerCase();
    if (["script", "style", "noscript", "template"].includes(tag)) return "";
    if (node.offsetParent === null && tag !== "body") return "";
    let t = "";
    for (const c of node.childNodes) t += nodeText(c);
    return t;
  }

  /** 取得元素的可讀文字（去掉多餘空白） */
  function elementText(el) {
    return nodeText(el).replace(/\s+/g, " ").trim();
  }

  /** 過濾出可朗讀的區塊 */
  function collectReadableNodes(container) {
    const selectors =
      ".guide h2, .guide h3, .guide h4, .guide p, " +
      ".guide li, .guide td, .guide th, .guide blockquote, " +
      ".guide .callout, .guide .outcome, " +
      ".guide .demo-block > pre, .guide .demo-block > .demo-render";
    const nodes = Array.from(container.querySelectorAll(selectors));
    // 只保留有實質文字的
    return nodes.filter((n) => {
      const t = elementText(n);
      return t.length > 0;
    });
  }

  /* ============================================================
   *  SpeechManager 核心
   * ============================================================ */

  class SpeechManager {
    constructor() {
      this.synth = window.speechSynthesis;
      this.utterance = null;
      this.nodes = [];         // 可朗讀的 DOM nodes
      this.currentIndex = -1;
      this.playing = false;
      this.paused = false;
      this.rate = 1;
      this.voiceUri = "";      // 選擇的 voice URI
      this.langMode = "zh";    // "zh" | "en" | "both"
      this.cancelled = false;

      // 偵測可用語音
      this.zhVoices = [];
      this.enVoices = [];
      this._loadVoices();

      // 如果 speechSynthesis 的 voices 還沒載入完，等事件
      if (this.synth.onvoiceschanged !== undefined) {
        this.synth.onvoiceschanged = () => this._loadVoices();
      }
    }

    /* ---------- 語音列表 ---------- */
    _loadVoices() {
      const all = this.synth.getVoices();
      this.zhVoices = all.filter(
        (v) => v.lang.startsWith("zh") || v.lang.startsWith("cmn")
      );
      this.enVoices = all.filter((v) => v.lang.startsWith("en"));
      this.allVoices = [...this.zhVoices, ...this.enVoices];
      this._populateVoiceSelect();
    }

    _populateVoiceSelect() {
      const sel = document.getElementById("speech-voice-select");
      if (!sel) return;
      sel.innerHTML = "";
      const addGroup = (label, voices) => {
        if (!voices.length) return;
        const grp = document.createElement("optgroup");
        grp.label = label;
        voices.forEach((v) => {
          const opt = document.createElement("option");
          opt.value = v.voiceURI;
          opt.textContent = `${v.name} (${v.lang})`;
          grp.appendChild(opt);
        });
        sel.appendChild(grp);
      };
      addGroup("中文", this.zhVoices);
      addGroup("English", this.enVoices);
      // 預選第一個中文語音
      if (this.zhVoices.length && !this.voiceUri) {
        this.voiceUri = this.zhVoices[0].voiceURI;
        sel.value = this.voiceUri;
      }
    }

    /* ---------- 初始化 nodes ---------- */
    init() {
      const container = document.querySelector(".guide") || document.querySelector(".container");
      if (!container) return;
      this.nodes = collectReadableNodes(container);
    }

    /* ---------- 取得當前語音物件 ---------- */
    _getVoice() {
      const all = this.synth.getVoices();
      return all.find((v) => v.voiceURI === this.voiceUri) || all[0] || null;
    }

    /* ---------- 朗讀一段文字 ---------- */
    _speakText(text, onEnd) {
      // 取消之前的
      this.synth.cancel();

      const utt = new SpeechSynthesisUtterance(text);
      const voice = this._getVoice();
      if (voice) {
        utt.voice = voice;
        utt.lang = voice.lang;
      }
      utt.rate = this.rate;
      utt.pitch = 1;

      utt.onend = () => {
        if (!this.cancelled) onEnd();
      };
      utt.onerror = (e) => {
        if (e.error !== "canceled" && !this.cancelled) onEnd();
      };

      this.utterance = utt;
      this.synth.speak(utt);
    }

    /* ---------- 判斷這段文字該用什麼語言 ---------- */
    _pickLang(text) {
      if (this.langMode === "zh") return "zh";
      if (this.langMode === "en") return "en";
      // "both" — 偵測
      return isMostlyChinese(text) ? "zh" : "en";
    }

    /* ---------- 檢查是否在 .pair 雙語區 ---------- */
    _inPairZone(node) {
      return node.closest(".pair") || node.closest(".col-en") || node.closest(".col-zh");
    }

    /* ---------- 針對雙語區的文字提取 ---------- */
    _getTextForNode(node, lang) {
      const pair = node.closest(".pair");
      if (!pair) return elementText(node);

      // 雙語區：根據語言模式選擇
      if (lang === "zh") {
        const zhCol = pair.querySelector(".col-zh");
        return zhCol ? elementText(zhCol) : elementText(node);
      } else {
        const enCol = pair.querySelector(".col-en");
        return enCol ? elementText(enCol) : elementText(node);
      }
    }

    /* ============================================================
     *  播放控制
     * ============================================================ */

    play() {
      if (this.nodes.length === 0) this.init();
      if (this.nodes.length === 0) return;

      if (this.paused) {
        this.synth.resume();
        this.paused = false;
        this.playing = true;
        this._updateUI();
        return;
      }

      // 從頭或從目前位置開始
      if (this.currentIndex < 0) this.currentIndex = 0;
      this.cancelled = false;
      this.playing = true;
      this._speakNode(this.currentIndex);
      this._updateUI();
    }

    _speakNode(index) {
      if (index >= this.nodes.length) {
        this.stop();
        return;
      }

      this.currentIndex = index;
      const node = this.nodes[index];
      const text = elementText(node);

      // 跳過空白段
      if (!text) {
        this._speakNode(index + 1);
        return;
      }

      // 高亮
      this._highlight(node);

      // 判斷語言
      const lang = this._pickLang(text);
      const speakText = this._getTextForNode(node, lang);

      this._speakText(speakText, () => {
        this._unhighlight(node);
        if (this.playing && !this.cancelled) {
          this._speakNode(index + 1);
        }
      });

      this._updateStatus(`朗讀中… (${index + 1}/${this.nodes.length})`);
    }

    pause() {
      if (this.playing && !this.paused) {
        this.synth.pause();
        this.paused = true;
        this.playing = true;
        this._updateUI();
        this._updateStatus("已暫停");
      }
    }

    stop() {
      this.cancelled = true;
      this.synth.cancel();
      this.playing = false;
      this.paused = false;
      // 移除所有高亮
      document.querySelectorAll(".speech-highlight").forEach((el) => {
        el.classList.remove("speech-highlight");
      });
      this._updateUI();
      this._updateStatus("已停止");
    }

    /* ---------- 高亮 ---------- */
    _highlight(node) {
      // 移除上一段高亮
      document.querySelectorAll(".speech-highlight").forEach((el) => {
        el.classList.remove("speech-highlight");
      });
      node.classList.add("speech-highlight");
      // 滾動到可見位置
      node.scrollIntoView({ behavior: "smooth", block: "center" });
    }

    _unhighlight(node) {
      node.classList.remove("speech-highlight");
    }

    /* ---------- UI 更新 ---------- */
    _updateUI() {
      const playBtn = document.getElementById("speech-play");
      if (playBtn) {
        if (this.playing && !this.paused) {
          playBtn.textContent = "⏸";
          playBtn.classList.add("active");
          playBtn.title = "暫停";
        } else {
          playBtn.textContent = "▶";
          playBtn.classList.remove("active");
          playBtn.title = "播放";
        }
      }
    }

    _updateStatus(text) {
      const el = document.getElementById("speech-status");
      if (el) el.textContent = text;
    }
  }

  /* ============================================================
   *  建立 DOM
   * ============================================================ */

  function createPanel(sm) {
    // 如果瀏覽器不支援
    if (!("speechSynthesis" in window)) {
      const div = document.createElement("div");
      div.className = "speech-unsupported";
      div.textContent = "此瀏覽器不支援語音朗讀";
      document.body.appendChild(div);
      return;
    }

    // --- 浮動開關按鈕 ---
    const toggle = document.createElement("button");
    toggle.className = "speech-toggle";
    toggle.innerHTML = "🔊";
    toggle.title = "語音朗讀";
    document.body.appendChild(toggle);

    // --- 控制面板 ---
    const panel = document.createElement("div");
    panel.className = "speech-panel speech-hidden";
    panel.innerHTML = `
      <div class="speech-row">
        <button id="speech-play" class="speech-btn" title="播放">▶</button>
        <button id="speech-stop" class="speech-btn stop" title="停止">⏹</button>
        <div class="speech-speed-wrap">
          <label>語速</label>
          <input type="range" id="speech-rate" min="0.5" max="2" step="0.25" value="1">
          <span id="speech-rate-val" class="speech-speed-val">1x</span>
        </div>
      </div>
      <div class="speech-row2">
        <select id="speech-voice-select" class="speech-select" title="選擇語音"></select>
      </div>
      <div class="speech-row2">
        <span style="font-size:0.66rem;color:#a3a1b6;">語言：</span>
        <div class="speech-lang-modes">
          <button class="speech-lang-btn active" data-lang="zh">中文</button>
          <button class="speech-lang-btn" data-lang="en">English</button>
          <button class="speech-lang-btn" data-lang="both">雙語</button>
        </div>
      </div>
      <div id="speech-status" class="speech-status"></div>
      <div class="speech-hotkeys">
        <span><kbd>Space</kbd> 播放/暫停</span>
        <span><kbd>Esc</kbd> 停止</span>
      </div>
    `;
    document.body.appendChild(panel);

    /* ---------- 事件綁定 ---------- */

    // 展開/收合（單一 handler）
    toggle.addEventListener("click", () => {
      const isHidden = panel.classList.contains("speech-hidden");
      if (isHidden) {
        panel.classList.remove("speech-hidden");
        toggle.classList.add("panel-open");
      } else {
        panel.classList.add("speech-hidden");
        toggle.classList.remove("panel-open");
      }
    });

    // 播放/暫停
    document.getElementById("speech-play").addEventListener("click", () => {
      if (sm.playing && !sm.paused) {
        sm.pause();
      } else {
        sm.play();
      }
    });

    // 停止
    document.getElementById("speech-stop").addEventListener("click", () => {
      sm.stop();
    });

    // 語速
    const rateInput = document.getElementById("speech-rate");
    const rateVal = document.getElementById("speech-rate-val");
    rateInput.addEventListener("input", () => {
      sm.rate = parseFloat(rateInput.value);
      rateVal.textContent = sm.rate + "x";
    });

    // 語音選擇
    document.getElementById("speech-voice-select").addEventListener("change", (e) => {
      sm.voiceUri = e.target.value;
    });

    // 語言模式
    document.querySelectorAll(".speech-lang-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        document.querySelectorAll(".speech-lang-btn").forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        sm.langMode = btn.dataset.lang;
      });
    });

    // 快捷鍵
    document.addEventListener("keydown", (e) => {
      // 忽略在 input / textarea 內的按鍵
      if (["INPUT", "TEXTAREA", "SELECT"].includes(e.target.tagName)) return;
      if (e.target.isContentEditable) return;

      if (e.code === "Space") {
        e.preventDefault();
        if (sm.playing && !sm.paused) {
          sm.pause();
        } else {
          sm.play();
        }
      } else if (e.key === "Escape") {
        sm.stop();
      }
    });
  }

  /* ============================================================
   *  啟動
   * ============================================================ */

  function boot() {
    const sm = new SpeechManager();
    createPanel(sm);
    // 預先初始化
    sm.init();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
