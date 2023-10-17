/*! For license information please see 61231-D2_3JyskI3w.js.LICENSE.txt */
export const id=61231;export const ids=[61231];export const modules={14095:(e,t,a)=>{a(56299),a(65660);var i=a(26110),r=a(98235),o=a(9672),n=a(69491),s=a(50856);(0,o.k)({_template:s.d`
    <style>
      :host {
        display: inline-block;
        position: relative;
        width: 400px;
        border: 1px solid;
        padding: 2px;
        -moz-appearance: textarea;
        -webkit-appearance: textarea;
        overflow: hidden;
      }

      .mirror-text {
        visibility: hidden;
        word-wrap: break-word;
        @apply --iron-autogrow-textarea;
      }

      .fit {
        @apply --layout-fit;
      }

      textarea {
        position: relative;
        outline: none;
        border: none;
        resize: none;
        background: inherit;
        color: inherit;
        /* see comments in template */
        width: 100%;
        height: 100%;
        font-size: inherit;
        font-family: inherit;
        line-height: inherit;
        text-align: inherit;
        @apply --iron-autogrow-textarea;
      }

      textarea::-webkit-input-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }

      textarea:-moz-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }

      textarea::-moz-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }

      textarea:-ms-input-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }
    </style>

    <!-- the mirror sizes the input/textarea so it grows with typing -->
    <!-- use &#160; instead &nbsp; of to allow this element to be used in XHTML -->
    <div id="mirror" class="mirror-text" aria-hidden="true">&nbsp;</div>

    <!-- size the input/textarea with a div, because the textarea has intrinsic size in ff -->
    <div class="textarea-container fit">
      <textarea id="textarea" name$="[[name]]" aria-label$="[[label]]" autocomplete$="[[autocomplete]]" autofocus$="[[autofocus]]" autocapitalize$="[[autocapitalize]]" inputmode$="[[inputmode]]" placeholder$="[[placeholder]]" readonly$="[[readonly]]" required$="[[required]]" disabled$="[[disabled]]" rows$="[[rows]]" minlength$="[[minlength]]" maxlength$="[[maxlength]]"></textarea>
    </div>
`,is:"iron-autogrow-textarea",behaviors:[r.x,i.a],properties:{value:{observer:"_valueChanged",type:String,notify:!0},bindValue:{observer:"_bindValueChanged",type:String,notify:!0},rows:{type:Number,value:1,observer:"_updateCached"},maxRows:{type:Number,value:0,observer:"_updateCached"},autocomplete:{type:String,value:"off"},autofocus:{type:Boolean,value:!1},autocapitalize:{type:String,value:"none"},inputmode:{type:String},placeholder:{type:String},readonly:{type:String},required:{type:Boolean},minlength:{type:Number},maxlength:{type:Number},label:{type:String}},listeners:{input:"_onInput"},get textarea(){return this.$.textarea},get selectionStart(){return this.$.textarea.selectionStart},get selectionEnd(){return this.$.textarea.selectionEnd},set selectionStart(e){this.$.textarea.selectionStart=e},set selectionEnd(e){this.$.textarea.selectionEnd=e},attached:function(){navigator.userAgent.match(/iP(?:[oa]d|hone)/)&&!navigator.userAgent.match(/OS 1[3456789]/)&&(this.$.textarea.style.marginLeft="-3px")},validate:function(){var e=this.$.textarea.validity.valid;return e&&(this.required&&""===this.value?e=!1:this.hasValidator()&&(e=r.x.validate.call(this,this.value))),this.invalid=!e,this.fire("iron-input-validate"),e},_bindValueChanged:function(e){this.value=e},_valueChanged:function(e){var t=this.textarea;t&&(t.value!==e&&(t.value=e||0===e?e:""),this.bindValue=e,this.$.mirror.innerHTML=this._valueForMirror(),this.fire("bind-value-changed",{value:this.bindValue}))},_onInput:function(e){var t=(0,n.vz)(e).path;this.value=t?t[0].value:e.target.value},_constrain:function(e){var t;for(e=e||[""],t=this.maxRows>0&&e.length>this.maxRows?e.slice(0,this.maxRows):e.slice(0);this.rows>0&&t.length<this.rows;)t.push("");return t.join("<br/>")+"&#160;"},_valueForMirror:function(){var e=this.textarea;if(e)return this.tokens=e&&e.value?e.value.replace(/&/gm,"&amp;").replace(/"/gm,"&quot;").replace(/'/gm,"&#39;").replace(/</gm,"&lt;").replace(/>/gm,"&gt;").split("\n"):[""],this._constrain(this.tokens)},_updateCached:function(){this.$.mirror.innerHTML=this._constrain(this.tokens)}});a(2178),a(98121),a(65911);var l=a(21006),d=a(66668);(0,o.k)({_template:s.d`
    <style>
      :host {
        display: block;
      }

      :host([hidden]) {
        display: none !important;
      }

      label {
        pointer-events: none;
      }
    </style>

    <paper-input-container no-label-float$="[[noLabelFloat]]" always-float-label="[[_computeAlwaysFloatLabel(alwaysFloatLabel,placeholder)]]" auto-validate$="[[autoValidate]]" disabled$="[[disabled]]" invalid="[[invalid]]">

      <label hidden$="[[!label]]" aria-hidden="true" for$="[[_inputId]]" slot="label">[[label]]</label>

      <iron-autogrow-textarea class="paper-input-input" slot="input" id$="[[_inputId]]" aria-labelledby$="[[_ariaLabelledBy]]" aria-describedby$="[[_ariaDescribedBy]]" bind-value="{{value}}" invalid="{{invalid}}" validator$="[[validator]]" disabled$="[[disabled]]" autocomplete$="[[autocomplete]]" autofocus$="[[autofocus]]" inputmode$="[[inputmode]]" name$="[[name]]" placeholder$="[[placeholder]]" readonly$="[[readonly]]" required$="[[required]]" minlength$="[[minlength]]" maxlength$="[[maxlength]]" autocapitalize$="[[autocapitalize]]" rows$="[[rows]]" max-rows$="[[maxRows]]" on-change="_onChange"></iron-autogrow-textarea>

      <template is="dom-if" if="[[errorMessage]]">
        <paper-input-error aria-live="assertive" slot="add-on">[[errorMessage]]</paper-input-error>
      </template>

      <template is="dom-if" if="[[charCounter]]">
        <paper-input-char-counter slot="add-on"></paper-input-char-counter>
      </template>

    </paper-input-container>
`,is:"paper-textarea",behaviors:[d.d0,l.V],properties:{_ariaLabelledBy:{observer:"_ariaLabelledByChanged",type:String},_ariaDescribedBy:{observer:"_ariaDescribedByChanged",type:String},value:{type:String},rows:{type:Number,value:1},maxRows:{type:Number,value:0}},get selectionStart(){return this.$.input.textarea.selectionStart},set selectionStart(e){this.$.input.textarea.selectionStart=e},get selectionEnd(){return this.$.input.textarea.selectionEnd},set selectionEnd(e){this.$.input.textarea.selectionEnd=e},_ariaLabelledByChanged:function(e){this._focusableElement.setAttribute("aria-labelledby",e)},_ariaDescribedByChanged:function(e){this._focusableElement.setAttribute("aria-describedby",e)},get _focusableElement(){return this.inputElement.textarea}})},54091:(e,t,a)=>{a.r(t),a.d(t,{HuiDialogReportProblemToAis:()=>d,ReportProblemToAisWs:()=>l});var i=a(17463),r=(a(14271),a(63436),a(44577),a(53973),a(51095),a(14095),a(68144)),o=a(79932),n=(a(31206),a(34821)),s=a(11654);const l=(e,t,a,i)=>e.callWS({type:"ais_cloud/report_ais_problem",problem_type:t,problem_desc:a,problem_data:i});let d=(0,i.Z)([(0,o.Mo)("hui-dialog-report-problem-to-ais")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"_params",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"_loading",value:()=>!1},{kind:"field",decorators:[(0,o.Cb)()],key:"_problemDescription",value:()=>""},{kind:"field",decorators:[(0,o.Cb)()],key:"_aisAnswer",value:void 0},{kind:"field",key:"_aisMediaInfo",value:void 0},{kind:"method",key:"showDialog",value:function(e){this._params=e,this._aisMediaInfo=this.hass.states["media_player.wbudowany_glosnik"],this._aisAnswer=void 0,this._problemDescription=""}},{kind:"method",key:"closeDialog",value:function(){this._params=void 0,this._aisAnswer=void 0,this._problemDescription=""}},{kind:"method",key:"render",value:function(){var e,t,a,i,o;return this._params?r.dy` <ha-dialog open hideActions .heading="${(0,n.i)(this.hass,"Zgłoszenie problemu ze źródłem multimediów")}" @closed="${this.closeDialog}"> ${this._loading?r.dy`<ha-circular-progress active></ha-circular-progress>`:r.dy``} ${this._loading?r.dy` <p> Wysyłam zgłoszenie do AIS </p>`:r.dy`<p> Problem z odtwarzaniem ${null===(e=this._aisMediaInfo)||void 0===e?void 0:e.attributes.source}, <b></b>${null===(t=this._aisMediaInfo)||void 0===t?void 0:t.attributes.media_title} <span class="aisUrl"> <br>z adresu URL <ha-icon icon="mdi:web"></ha-icon>: <b></b>${null===(a=this._aisMediaInfo)||void 0===a?void 0:a.attributes.media_content_id} </span> </p> <div class="img404"><img src="${null===(i=this._aisMediaInfo)||void 0===i?void 0:i.attributes.media_stream_image}"></div> ${this._aisAnswer?r.dy` <div style="text-align:center"> ${this._aisAnswer.error?r.dy` <h2> Podczas przesyłania zgłoszenia wystąpił problem </h2> <p> ${null===(o=this._aisAnswer)||void 0===o?void 0:o.message} </p> <p> Sprawdz połączenie z Internetem i spróbuj ponownie później. </p> `:r.dy` <h2> Przesłano zgłoszenie do AIS, o numerze: ${this._aisAnswer.report_id} </h2> <p> ${this._aisAnswer.message} </p> `} </div> <div class="sendProblemToAisButton"> <mwc-button raised @click="${this.closeDialog}"> <ha-icon icon="hass:close-thick"></ha-icon>  OK </mwc-button> </div> `:r.dy` <p> Wyślij zgłoszenie do AI-Speaker. Postaramy się jak najszybciej naprawić ten problem. </p> <paper-textarea label="Dodatkowy opis dla AI-Speaker" placeholder="Tu możesz np. podać nowy adres zasobu, jeżeli go znasz." name="description" .value="${this._problemDescription}" @value-changed="${this._handleProblemDescriptionChange}"></paper-textarea> <div class="sendProblemToAisButton"> <mwc-button raised @click="${this._handleReportProblemToAis}"> <ha-icon icon="hass:email-send"></ha-icon>  Wyślij zgłoszenie do AI-Speaker </mwc-button> </div>`}`} </ha-dialog>`:r.dy``}},{kind:"method",key:"_reportProblemToAis",value:async function(){this._loading=!0;let e={message:"",email:"",report_id:0,error:!1};try{var t,a;e=await l(this.hass,"media_source",this._problemDescription,(null===(t=this._aisMediaInfo)||void 0===t?void 0:t.attributes.media_title)+" "+(null===(a=this._aisMediaInfo)||void 0===a?void 0:a.attributes.media_content_id))}catch(t){e.message=t.message,e.error=!0,this._loading=!1}return this._loading=!1,e}},{kind:"method",key:"_handleReportProblemToAis",value:async function(){this._aisAnswer=await this._reportProblemToAis()}},{kind:"method",key:"_handleProblemDescriptionChange",value:function(e){this._problemDescription=e.detail.value}},{kind:"get",static:!0,key:"styles",value:function(){return[s.yu,r.iv`ha-dialog{--dialog-content-padding:0 24px 20px}div.sendProblemToAisButton{text-align:center;margin:10px}div.img404{text-align:center}img{max-width:500px;max-height:300px;-webkit-filter:grayscale(100%);filter:grayscale(100%)}span.aisUrl{word-wrap:break-word}ha-circular-progress{--mdc-theme-primary:var(--primary-color);display:flex;justify-content:center;margin-top:40px;margin-bottom:20px}`]}}]}}),r.oi)}};
//# sourceMappingURL=61231-D2_3JyskI3w.js.map