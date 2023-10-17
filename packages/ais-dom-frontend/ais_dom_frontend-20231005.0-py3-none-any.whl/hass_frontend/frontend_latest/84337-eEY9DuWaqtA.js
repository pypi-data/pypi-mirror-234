/*! For license information please see 84337-eEY9DuWaqtA.js.LICENSE.txt */
export const id=84337;export const ids=[84337];export const modules={39841:(e,t,i)=>{i(56299),i(65660);var o=i(9672),s=i(69491),a=i(50856),n=i(44181);(0,o.k)({_template:a.d`
    <style>
      :host {
        display: block;
        /**
         * Force app-header-layout to have its own stacking context so that its parent can
         * control the stacking of it relative to other elements (e.g. app-drawer-layout).
         * This could be done using \`isolation: isolate\`, but that's not well supported
         * across browsers.
         */
        position: relative;
        z-index: 0;
      }

      #wrapper ::slotted([slot=header]) {
        @apply --layout-fixed-top;
        z-index: 1;
      }

      #wrapper.initializing ::slotted([slot=header]) {
        position: relative;
      }

      :host([has-scrolling-region]) {
        height: 100%;
      }

      :host([has-scrolling-region]) #wrapper ::slotted([slot=header]) {
        position: absolute;
      }

      :host([has-scrolling-region]) #wrapper.initializing ::slotted([slot=header]) {
        position: relative;
      }

      :host([has-scrolling-region]) #wrapper #contentContainer {
        @apply --layout-fit;
        overflow-y: auto;
        -webkit-overflow-scrolling: touch;
      }

      :host([has-scrolling-region]) #wrapper.initializing #contentContainer {
        position: relative;
      }

      :host([fullbleed]) {
        @apply --layout-vertical;
        @apply --layout-fit;
      }

      :host([fullbleed]) #wrapper,
      :host([fullbleed]) #wrapper #contentContainer {
        @apply --layout-vertical;
        @apply --layout-flex;
      }

      #contentContainer {
        /* Create a stacking context here so that all children appear below the header. */
        position: relative;
        z-index: 0;
      }

      @media print {
        :host([has-scrolling-region]) #wrapper #contentContainer {
          overflow-y: visible;
        }
      }

    </style>

    <div id="wrapper" class="initializing">
      <slot id="headerSlot" name="header"></slot>

      <div id="contentContainer">
        <slot></slot>
      </div>
    </div>
`,is:"app-header-layout",behaviors:[n.Y],properties:{hasScrollingRegion:{type:Boolean,value:!1,reflectToAttribute:!0}},observers:["resetLayout(isAttached, hasScrollingRegion)"],get header(){return(0,s.vz)(this.$.headerSlot).getDistributedNodes()[0]},_updateLayoutStates:function(){var e=this.header;if(this.isAttached&&e){this.$.wrapper.classList.remove("initializing"),e.scrollTarget=this.hasScrollingRegion?this.$.contentContainer:this.ownerDocument.documentElement;var t=e.offsetHeight;this.hasScrollingRegion?(e.style.left="",e.style.right=""):requestAnimationFrame(function(){var t=this.getBoundingClientRect(),i=document.documentElement.clientWidth-t.right;e.style.left=t.left+"px",e.style.right=i+"px"}.bind(this));var i=this.$.contentContainer.style;e.fixed&&!e.condenses&&this.hasScrollingRegion?(i.marginTop=t+"px",i.paddingTop=""):(i.paddingTop=t+"px",i.marginTop="")}}})},53973:(e,t,i)=>{i(56299),i(65660),i(97968);var o=i(9672),s=i(50856),a=i(33760);(0,o.k)({_template:s.d`
    <style include="paper-item-shared-styles">
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
      }
    </style>
    <slot></slot>
`,is:"paper-item",behaviors:[a.U]})},81545:(e,t,i)=>{var o=i(17463),s=i(34541),a=i(47838),n=(i(65666),i(68144)),r=i(79932),l=i(74265);(0,o.Z)([(0,r.Mo)("ha-button-menu")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",key:l.gA,value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"corner",value:()=>"BOTTOM_START"},{kind:"field",decorators:[(0,r.Cb)()],key:"menuCorner",value:()=>"START"},{kind:"field",decorators:[(0,r.Cb)({type:Number})],key:"x",value:()=>null},{kind:"field",decorators:[(0,r.Cb)({type:Number})],key:"y",value:()=>null},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"multi",value:()=>!1},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"activatable",value:()=>!1},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"disabled",value:()=>!1},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"fixed",value:()=>!1},{kind:"field",decorators:[(0,r.IO)("mwc-menu",!0)],key:"_menu",value:void 0},{kind:"get",key:"items",value:function(){var e;return null===(e=this._menu)||void 0===e?void 0:e.items}},{kind:"get",key:"selected",value:function(){var e;return null===(e=this._menu)||void 0===e?void 0:e.selected}},{kind:"method",key:"focus",value:function(){var e,t;null!==(e=this._menu)&&void 0!==e&&e.open?this._menu.focusItemAtIndex(0):null===(t=this._triggerButton)||void 0===t||t.focus()}},{kind:"method",key:"render",value:function(){return n.dy` <div @click="${this._handleClick}"> <slot name="trigger" @slotchange="${this._setTriggerAria}"></slot> </div> <mwc-menu .corner="${this.corner}" .menuCorner="${this.menuCorner}" .fixed="${this.fixed}" .multi="${this.multi}" .activatable="${this.activatable}" .y="${this.y}" .x="${this.x}"> <slot></slot> </mwc-menu> `}},{kind:"method",key:"firstUpdated",value:function(e){(0,s.Z)((0,a.Z)(i.prototype),"firstUpdated",this).call(this,e),"rtl"===document.dir&&this.updateComplete.then((()=>{this.querySelectorAll("mwc-list-item").forEach((e=>{const t=document.createElement("style");t.innerHTML="span.material-icons:first-of-type { margin-left: var(--mdc-list-item-graphic-margin, 32px) !important; margin-right: 0px !important;}",e.shadowRoot.appendChild(t)}))}))}},{kind:"method",key:"_handleClick",value:function(){this.disabled||(this._menu.anchor=this,this._menu.show())}},{kind:"get",key:"_triggerButton",value:function(){return this.querySelector('ha-icon-button[slot="trigger"], mwc-button[slot="trigger"]')}},{kind:"method",key:"_setTriggerAria",value:function(){this._triggerButton&&(this._triggerButton.ariaHasPopup="menu")}},{kind:"get",static:!0,key:"styles",value:function(){return n.iv`:host{display:inline-block;position:relative}::slotted([disabled]){color:var(--disabled-text-color)}`}}]}}),n.oi)},94469:(e,t,i)=>{i.d(t,{j:()=>a});var o=i(47181);const s=()=>Promise.all([i.e(28426),i.e(28597),i.e(56299),i.e(97215),i.e(68200),i.e(88700),i.e(38538)]).then(i.bind(i,38538)),a=(e,t)=>{(0,o.B)(e,"show-dialog",{dialogTag:"dialog-ais-file",dialogImport:s,dialogParams:t})}},9535:(e,t,i)=>{i.r(t);var o=i(17463),s=(i(27289),i(12730),i(68144)),a=i(79932),n=(i(60010),i(38353),i(27213),i(47181)),r=(i(81545),i(44577),i(94469)),l=i(11654);(0,o.Z)([(0,a.Mo)("ha-config-ais-dom-config-tts")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.Cb)({type:Boolean})],key:"isWide",value:void 0},{kind:"field",decorators:[(0,a.Cb)({type:Boolean})],key:"narrow",value:()=>!1},{kind:"field",decorators:[(0,a.Cb)({type:String})],key:"selectedVoice",value:()=>""},{kind:"method",key:"firstUpdated",value:function(){this.selectedVoice=this.hass.states["input_select.assistant_voice"].state}},{kind:"method",key:"render",value:function(){return s.dy` <hass-subpage header="Konfiguracja bramki AIS dom"> <div .narrow="${this.narrow}"> <ha-config-section .isWide="${this.isWide}"> <span slot="header">Ustawienia głosu Asystenta</span> <span slot="introduction">Możesz zmienić głos asystenta i dostosować szybkość i ton mowy oraz komunikat mówiony przez asystenta podczas startu systemu..</span> <ha-card header="Wybór głosu Asystenta"> <div class="card-content"> <div class="person"> <img class="${this.personImgClass(this.selectedVoice,"Jola online")}" data-voice="Jola online" alt="Jola Online" title="Jola Online" @click="${this.switchTtsPerson}" src="/static/ais_dom/Ania.jpg"> </div> <div class="person"> <img class="${this.personImgClass(this.selectedVoice,"Jola lokalnie")}" data-voice="Jola lokalnie" alt="Jola Lokalnie" title="Jola Lokalnie" @click="${this.switchTtsPerson}" src="/static/ais_dom/Asia.jpg"> </div> <div class="person"> <img class="${this.personImgClass(this.selectedVoice,"Celina")}" data-voice="Celina" alt="Celina" title="Celina" @click="${this.switchTtsPerson}" src="/static/ais_dom/Celka.jpg"> </div> <div class="person"> <img class="${this.personImgClass(this.selectedVoice,"Anżela")}" data-voice="Anżela" alt="Anżela" title="Anżela" @click="${this.switchTtsPerson}" src="/static/ais_dom/Anzela.jpg"> </div> <div class="person"> <img class="${this.personImgClass(this.selectedVoice,"Asia")}" data-voice="Asia" alt="Asia" title="Asia" @click="${this.switchTtsPerson}" src="/static/ais_dom/Kasia.jpg"> </div> <div class="person"> <img class="${this.personImgClass(this.selectedVoice,"Sebastian")}" data-voice="Sebastian" alt="Sebastian" title="Sebastian" @click="${this.switchTtsPerson}" src="/static/ais_dom/Sebastian.jpg"> </div> <div class="person"> <img class="${this.personImgClass(this.selectedVoice,"Bartek")}" data-voice="Bartek" alt="Bartek" title="Bartek" @click="${this.switchTtsPerson}" src="/static/ais_dom/Bartek.jpg"> </div> <div class="person"> <img class="${this.personImgClass(this.selectedVoice,"Andrzej")}" data-voice="Andrzej" alt="Andrzej" title="Andrzej" @click="${this.switchTtsPerson}" src="/static/ais_dom/Andrzej.jpg"> </div> </div> <div class="card-actions person-actions"> <div @click="${this.tuneVoiceTone}"> <mwc-button> <ha-icon class="user-button" icon="hass:tune"></ha-icon>  Ton mowy</mwc-button> </div> <div @click="${this.tuneVoiceSpeed}"> <mwc-button> <ha-icon class="user-button" icon="hass:play-speed"></ha-icon>  Szybkość mowy </mwc-button> </div> <div @click="${this._openAisWelcomeText}"> <mwc-button> <ha-icon class="user-button" icon="hass:file-document-edit-outline"></ha-icon>  Welcome.txt</mwc-button> </div> </div> </ha-card> </ha-config-section> </div> </hass-subpage> `}},{kind:"get",static:!0,key:"styles",value:function(){return[l.Qx,s.iv`.content{padding-bottom:32px}.border{margin:32px auto 0;border-bottom:1px solid rgba(0,0,0,.12);max-width:1040px}.narrow .border{max-width:640px}.card-actions{display:flex}ha-card>paper-toggle-button{margin:-4px 0;position:absolute;top:32px;right:8px}.center-container{@apply --layout-vertical;@apply --layout-center-center;height:70px}div.person{display:inline-block;margin:10px}img{border-radius:50%;width:100px;height:100px;border:20px}img.person-img-selected{border:7px solid var(--primary-color);width:110px;height:110px}`]}},{kind:"method",key:"_openAisWelcomeText",value:async function(){const e="/data/data/com.termux/files/home/AIS/ais_welcome.txt",t={dialogTitle:"Edit ais_welcome.txt",filePath:e,fileBody:await this.hass.callApi("POST","ais_file/read",{filePath:e}),readonly:!1};(0,r.j)(this,t)}},{kind:"method",key:"computeClasses",value:function(e){return e?"content":"content narrow"}},{kind:"method",key:"personImgClass",value:function(e,t){return e===t?"person-img-selected":""}},{kind:"method",key:"tuneVoiceSpeed",value:function(){(0,n.B)(this,"hass-more-info",{entityId:"input_number.assistant_rate"})}},{kind:"method",key:"tuneVoiceTone",value:function(){(0,n.B)(this,"hass-more-info",{entityId:"input_number.assistant_tone"})}},{kind:"method",key:"switchTtsPerson",value:function(e){this.selectedVoice=e.target.dataset.voice,this.hass.callService("input_select","select_option",{entity_id:"input_select.assistant_voice",option:e.target.dataset.voice})}}]}}),s.oi)},82160:(e,t,i)=>{function o(e){return new Promise(((t,i)=>{e.oncomplete=e.onsuccess=()=>t(e.result),e.onabort=e.onerror=()=>i(e.error)}))}function s(e,t){const i=indexedDB.open(e);i.onupgradeneeded=()=>i.result.createObjectStore(t);const s=o(i);return(e,i)=>s.then((o=>i(o.transaction(t,e).objectStore(t))))}let a;function n(){return a||(a=s("keyval-store","keyval")),a}function r(e,t=n()){return t("readonly",(t=>o(t.get(e))))}function l(e,t,i=n()){return i("readwrite",(i=>(i.put(t,e),o(i.transaction))))}function c(e=n()){return e("readwrite",(e=>(e.clear(),o(e.transaction))))}i.d(t,{MT:()=>s,RV:()=>o,U2:()=>r,ZH:()=>c,t8:()=>l})}};
//# sourceMappingURL=84337-eEY9DuWaqtA.js.map