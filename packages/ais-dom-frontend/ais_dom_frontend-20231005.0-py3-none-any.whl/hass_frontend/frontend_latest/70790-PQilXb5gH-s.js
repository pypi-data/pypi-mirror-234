/*! For license information please see 70790-PQilXb5gH-s.js.LICENSE.txt */
export const id=70790;export const ids=[70790];export const modules={58014:(t,i,e)=>{function n(t,i){if(t.closest)return t.closest(i);for(var e=t;e;){if(o(e,i))return e;e=e.parentElement}return null}function o(t,i){return(t.matches||t.webkitMatchesSelector||t.msMatchesSelector).call(t,i)}e.d(i,{oq:()=>n,wB:()=>o})},18601:(t,i,e)=>{e.d(i,{Wg:()=>l,qN:()=>r.q});var n,o,a=e(87480),s=e(79932),r=e(78220);const c=null!==(o=null===(n=window.ShadyDOM)||void 0===n?void 0:n.inUse)&&void 0!==o&&o;class l extends r.H{constructor(){super(...arguments),this.disabled=!1,this.containingForm=null,this.formDataListener=t=>{this.disabled||this.setFormData(t.formData)}}findFormElement(){if(!this.shadowRoot||c)return null;const t=this.getRootNode().querySelectorAll("form");for(const i of Array.from(t))if(i.contains(this))return i;return null}connectedCallback(){var t;super.connectedCallback(),this.containingForm=this.findFormElement(),null===(t=this.containingForm)||void 0===t||t.addEventListener("formdata",this.formDataListener)}disconnectedCallback(){var t;super.disconnectedCallback(),null===(t=this.containingForm)||void 0===t||t.removeEventListener("formdata",this.formDataListener),this.containingForm=null}click(){this.formElement&&!this.disabled&&(this.formElement.focus(),this.formElement.click())}firstUpdated(){super.firstUpdated(),this.shadowRoot&&this.mdcRoot.addEventListener("change",(t=>{this.dispatchEvent(new Event("change",t))}))}}l.shadowRootOptions={mode:"open",delegatesFocus:!0},(0,a.__decorate)([(0,s.Cb)({type:Boolean})],l.prototype,"disabled",void 0)},20210:(t,i,e)=>{var n=e(87480),o=e(79932),a=(e(27763),e(38103)),s=e(98734),r=e(68144),c=e(30153);class l extends r.oi{constructor(){super(...arguments),this.disabled=!1,this.icon="",this.shouldRenderRipple=!1,this.rippleHandlers=new s.A((()=>(this.shouldRenderRipple=!0,this.ripple)))}renderRipple(){return this.shouldRenderRipple?r.dy` <mwc-ripple .disabled="${this.disabled}" unbounded> </mwc-ripple>`:""}focus(){const t=this.buttonElement;t&&(this.rippleHandlers.startFocus(),t.focus())}blur(){const t=this.buttonElement;t&&(this.rippleHandlers.endFocus(),t.blur())}render(){return r.dy`<button class="mdc-icon-button mdc-icon-button--display-flex" aria-label="${this.ariaLabel||this.icon}" aria-haspopup="${(0,c.o)(this.ariaHasPopup)}" ?disabled="${this.disabled}" @focus="${this.handleRippleFocus}" @blur="${this.handleRippleBlur}" @mousedown="${this.handleRippleMouseDown}" @mouseenter="${this.handleRippleMouseEnter}" @mouseleave="${this.handleRippleMouseLeave}" @touchstart="${this.handleRippleTouchStart}" @touchend="${this.handleRippleDeactivate}" @touchcancel="${this.handleRippleDeactivate}">${this.renderRipple()} ${this.icon?r.dy`<i class="material-icons">${this.icon}</i>`:""} <span><slot></slot></span> </button>`}handleRippleMouseDown(t){const i=()=>{window.removeEventListener("mouseup",i),this.handleRippleDeactivate()};window.addEventListener("mouseup",i),this.rippleHandlers.startPress(t)}handleRippleTouchStart(t){this.rippleHandlers.startPress(t)}handleRippleDeactivate(){this.rippleHandlers.endPress()}handleRippleMouseEnter(){this.rippleHandlers.startHover()}handleRippleMouseLeave(){this.rippleHandlers.endHover()}handleRippleFocus(){this.rippleHandlers.startFocus()}handleRippleBlur(){this.rippleHandlers.endFocus()}}(0,n.__decorate)([(0,o.Cb)({type:Boolean,reflect:!0})],l.prototype,"disabled",void 0),(0,n.__decorate)([(0,o.Cb)({type:String})],l.prototype,"icon",void 0),(0,n.__decorate)([a.L,(0,o.Cb)({type:String,attribute:"aria-label"})],l.prototype,"ariaLabel",void 0),(0,n.__decorate)([a.L,(0,o.Cb)({type:String,attribute:"aria-haspopup"})],l.prototype,"ariaHasPopup",void 0),(0,n.__decorate)([(0,o.IO)("button")],l.prototype,"buttonElement",void 0),(0,n.__decorate)([(0,o.GC)("mwc-ripple")],l.prototype,"ripple",void 0),(0,n.__decorate)([(0,o.SB)()],l.prototype,"shouldRenderRipple",void 0),(0,n.__decorate)([(0,o.hO)({passive:!0})],l.prototype,"handleRippleMouseDown",null),(0,n.__decorate)([(0,o.hO)({passive:!0})],l.prototype,"handleRippleTouchStart",null);const d=r.iv`.material-icons{font-family:var(--mdc-icon-font, "Material Icons");font-weight:400;font-style:normal;font-size:var(--mdc-icon-size,24px);line-height:1;letter-spacing:normal;text-transform:none;display:inline-block;white-space:nowrap;word-wrap:normal;direction:ltr;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;-moz-osx-font-smoothing:grayscale;font-feature-settings:"liga"}.mdc-icon-button{font-size:24px;width:48px;height:48px;padding:12px}.mdc-icon-button .mdc-icon-button__focus-ring{display:none}.mdc-icon-button.mdc-ripple-upgraded--background-focused .mdc-icon-button__focus-ring,.mdc-icon-button:not(.mdc-ripple-upgraded):focus .mdc-icon-button__focus-ring{display:block;max-height:48px;max-width:48px}@media screen and (forced-colors:active){.mdc-icon-button.mdc-ripple-upgraded--background-focused .mdc-icon-button__focus-ring,.mdc-icon-button:not(.mdc-ripple-upgraded):focus .mdc-icon-button__focus-ring{pointer-events:none;border:2px solid transparent;border-radius:6px;box-sizing:content-box;position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);height:100%;width:100%}}@media screen and (forced-colors:active)and (forced-colors:active){.mdc-icon-button.mdc-ripple-upgraded--background-focused .mdc-icon-button__focus-ring,.mdc-icon-button:not(.mdc-ripple-upgraded):focus .mdc-icon-button__focus-ring{border-color:CanvasText}}@media screen and (forced-colors:active){.mdc-icon-button.mdc-ripple-upgraded--background-focused .mdc-icon-button__focus-ring::after,.mdc-icon-button:not(.mdc-ripple-upgraded):focus .mdc-icon-button__focus-ring::after{content:"";border:2px solid transparent;border-radius:8px;display:block;position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);height:calc(100% + 4px);width:calc(100% + 4px)}}@media screen and (forced-colors:active)and (forced-colors:active){.mdc-icon-button.mdc-ripple-upgraded--background-focused .mdc-icon-button__focus-ring::after,.mdc-icon-button:not(.mdc-ripple-upgraded):focus .mdc-icon-button__focus-ring::after{border-color:CanvasText}}.mdc-icon-button.mdc-icon-button--reduced-size .mdc-icon-button__ripple{width:40px;height:40px;margin-top:4px;margin-bottom:4px;margin-right:4px;margin-left:4px}.mdc-icon-button.mdc-icon-button--reduced-size.mdc-ripple-upgraded--background-focused .mdc-icon-button__focus-ring,.mdc-icon-button.mdc-icon-button--reduced-size:not(.mdc-ripple-upgraded):focus .mdc-icon-button__focus-ring{max-height:40px;max-width:40px}.mdc-icon-button .mdc-icon-button__touch{position:absolute;top:50%;height:48px;left:50%;width:48px;transform:translate(-50%,-50%)}.mdc-icon-button:disabled{color:rgba(0,0,0,.38);color:var(--mdc-theme-text-disabled-on-light,rgba(0,0,0,.38))}.mdc-icon-button img,.mdc-icon-button svg{width:24px;height:24px}.mdc-icon-button{display:inline-block;position:relative;box-sizing:border-box;border:none;outline:0;background-color:transparent;fill:currentColor;color:inherit;text-decoration:none;cursor:pointer;user-select:none;z-index:0;overflow:visible}.mdc-icon-button .mdc-icon-button__touch{position:absolute;top:50%;height:48px;left:50%;width:48px;transform:translate(-50%,-50%)}.mdc-icon-button:disabled{cursor:default;pointer-events:none}.mdc-icon-button--display-flex{align-items:center;display:inline-flex;justify-content:center}.mdc-icon-button__icon{display:inline-block}.mdc-icon-button__icon.mdc-icon-button__icon--on{display:none}.mdc-icon-button--on .mdc-icon-button__icon{display:none}.mdc-icon-button--on .mdc-icon-button__icon.mdc-icon-button__icon--on{display:inline-block}.mdc-icon-button__link{height:100%;left:0;outline:0;position:absolute;top:0;width:100%}.mdc-icon-button{display:inline-block;position:relative;box-sizing:border-box;border:none;outline:0;background-color:transparent;fill:currentColor;color:inherit;text-decoration:none;cursor:pointer;user-select:none;z-index:0;overflow:visible}.mdc-icon-button .mdc-icon-button__touch{position:absolute;top:50%;height:48px;left:50%;width:48px;transform:translate(-50%,-50%)}.mdc-icon-button:disabled{cursor:default;pointer-events:none}.mdc-icon-button--display-flex{align-items:center;display:inline-flex;justify-content:center}.mdc-icon-button__icon{display:inline-block}.mdc-icon-button__icon.mdc-icon-button__icon--on{display:none}.mdc-icon-button--on .mdc-icon-button__icon{display:none}.mdc-icon-button--on .mdc-icon-button__icon.mdc-icon-button__icon--on{display:inline-block}.mdc-icon-button__link{height:100%;left:0;outline:0;position:absolute;top:0;width:100%}:host{display:inline-block;outline:0}:host([disabled]){pointer-events:none}.mdc-icon-button ::slotted(*),.mdc-icon-button i,.mdc-icon-button img,.mdc-icon-button svg{display:block}:host{--mdc-ripple-color:currentcolor;-webkit-tap-highlight-color:transparent}.mdc-icon-button,:host{vertical-align:top}.mdc-icon-button{width:var(--mdc-icon-button-size,48px);height:var(--mdc-icon-button-size,48px);padding:calc((var(--mdc-icon-button-size,48px) - var(--mdc-icon-size,24px))/ 2)}.mdc-icon-button ::slotted(*),.mdc-icon-button i,.mdc-icon-button img,.mdc-icon-button svg{display:block;width:var(--mdc-icon-size,24px);height:var(--mdc-icon-size,24px)}`;let p=class extends l{};p.styles=[d],p=(0,n.__decorate)([(0,o.Mo)("mwc-icon-button")],p)},44577:(t,i,e)=>{var n=e(87480),o=e(79932),a=e(61092),s=e(96762);let r=class extends a.K{};r.styles=[s.W],r=(0,n.__decorate)([(0,o.Mo)("mwc-list-item")],r)},54444:(t,i,e)=>{e(56299);var n=e(9672),o=e(69491),a=e(50856);(0,n.k)({_template:a.d`
    <style>
      :host {
        display: block;
        position: absolute;
        outline: none;
        z-index: 1002;
        -moz-user-select: none;
        -ms-user-select: none;
        -webkit-user-select: none;
        user-select: none;
        cursor: default;
      }

      #tooltip {
        display: block;
        outline: none;
        @apply --paper-font-common-base;
        font-size: 10px;
        line-height: 1;
        background-color: var(--paper-tooltip-background, #616161);
        color: var(--paper-tooltip-text-color, white);
        padding: 8px;
        border-radius: 2px;
        @apply --paper-tooltip;
      }

      @keyframes keyFrameScaleUp {
        0% {
          transform: scale(0.0);
        }
        100% {
          transform: scale(1.0);
        }
      }

      @keyframes keyFrameScaleDown {
        0% {
          transform: scale(1.0);
        }
        100% {
          transform: scale(0.0);
        }
      }

      @keyframes keyFrameFadeInOpacity {
        0% {
          opacity: 0;
        }
        100% {
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
      }

      @keyframes keyFrameFadeOutOpacity {
        0% {
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
        100% {
          opacity: 0;
        }
      }

      @keyframes keyFrameSlideDownIn {
        0% {
          transform: translateY(-2000px);
          opacity: 0;
        }
        10% {
          opacity: 0.2;
        }
        100% {
          transform: translateY(0);
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
      }

      @keyframes keyFrameSlideDownOut {
        0% {
          transform: translateY(0);
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
        10% {
          opacity: 0.2;
        }
        100% {
          transform: translateY(-2000px);
          opacity: 0;
        }
      }

      .fade-in-animation {
        opacity: 0;
        animation-delay: var(--paper-tooltip-delay-in, 500ms);
        animation-name: keyFrameFadeInOpacity;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-in, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .fade-out-animation {
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 0ms);
        animation-name: keyFrameFadeOutOpacity;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .scale-up-animation {
        transform: scale(0);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-in, 500ms);
        animation-name: keyFrameScaleUp;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-in, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .scale-down-animation {
        transform: scale(1);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameScaleDown;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .slide-down-animation {
        transform: translateY(-2000px);
        opacity: 0;
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameSlideDownIn;
        animation-iteration-count: 1;
        animation-timing-function: cubic-bezier(0.0, 0.0, 0.2, 1);
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .slide-down-animation-out {
        transform: translateY(0);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameSlideDownOut;
        animation-iteration-count: 1;
        animation-timing-function: cubic-bezier(0.4, 0.0, 1, 1);
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .cancel-animation {
        animation-delay: -30s !important;
      }

      /* Thanks IE 10. */

      .hidden {
        display: none !important;
      }
    </style>

    <div id="tooltip" class="hidden">
      <slot></slot>
    </div>
`,is:"paper-tooltip",hostAttributes:{role:"tooltip",tabindex:-1},properties:{for:{type:String,observer:"_findTarget"},manualMode:{type:Boolean,value:!1,observer:"_manualModeChanged"},position:{type:String,value:"bottom"},fitToVisibleBounds:{type:Boolean,value:!1},offset:{type:Number,value:14},marginTop:{type:Number,value:14},animationDelay:{type:Number,value:500,observer:"_delayChange"},animationEntry:{type:String,value:""},animationExit:{type:String,value:""},animationConfig:{type:Object,value:function(){return{entry:[{name:"fade-in-animation",node:this,timing:{delay:0}}],exit:[{name:"fade-out-animation",node:this}]}}},_showing:{type:Boolean,value:!1}},listeners:{webkitAnimationEnd:"_onAnimationEnd"},get target(){var t=(0,o.vz)(this).parentNode,i=(0,o.vz)(this).getOwnerRoot();return this.for?(0,o.vz)(i).querySelector("#"+this.for):t.nodeType==Node.DOCUMENT_FRAGMENT_NODE?i.host:t},attached:function(){this._findTarget()},detached:function(){this.manualMode||this._removeListeners()},playAnimation:function(t){"entry"===t?this.show():"exit"===t&&this.hide()},cancelAnimation:function(){this.$.tooltip.classList.add("cancel-animation")},show:function(){if(!this._showing){if(""===(0,o.vz)(this).textContent.trim()){for(var t=!0,i=(0,o.vz)(this).getEffectiveChildNodes(),e=0;e<i.length;e++)if(""!==i[e].textContent.trim()){t=!1;break}if(t)return}this._showing=!0,this.$.tooltip.classList.remove("hidden"),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.updatePosition(),this._animationPlaying=!0,this.$.tooltip.classList.add(this._getAnimationType("entry"))}},hide:function(){if(this._showing){if(this._animationPlaying)return this._showing=!1,void this._cancelAnimation();this._onAnimationFinish(),this._showing=!1,this._animationPlaying=!0}},updatePosition:function(){if(this._target&&this.offsetParent){var t=this.offset;14!=this.marginTop&&14==this.offset&&(t=this.marginTop);var i,e,n=this.offsetParent.getBoundingClientRect(),o=this._target.getBoundingClientRect(),a=this.getBoundingClientRect(),s=(o.width-a.width)/2,r=(o.height-a.height)/2,c=o.left-n.left,l=o.top-n.top;switch(this.position){case"top":i=c+s,e=l-a.height-t;break;case"bottom":i=c+s,e=l+o.height+t;break;case"left":i=c-a.width-t,e=l+r;break;case"right":i=c+o.width+t,e=l+r}this.fitToVisibleBounds?(n.left+i+a.width>window.innerWidth?(this.style.right="0px",this.style.left="auto"):(this.style.left=Math.max(0,i)+"px",this.style.right="auto"),n.top+e+a.height>window.innerHeight?(this.style.bottom=n.height-l+t+"px",this.style.top="auto"):(this.style.top=Math.max(-n.top,e)+"px",this.style.bottom="auto")):(this.style.left=i+"px",this.style.top=e+"px")}},_addListeners:function(){this._target&&(this.listen(this._target,"mouseenter","show"),this.listen(this._target,"focus","show"),this.listen(this._target,"mouseleave","hide"),this.listen(this._target,"blur","hide"),this.listen(this._target,"tap","hide")),this.listen(this.$.tooltip,"animationend","_onAnimationEnd"),this.listen(this,"mouseenter","hide")},_findTarget:function(){this.manualMode||this._removeListeners(),this._target=this.target,this.manualMode||this._addListeners()},_delayChange:function(t){500!==t&&this.updateStyles({"--paper-tooltip-delay-in":t+"ms"})},_manualModeChanged:function(){this.manualMode?this._removeListeners():this._addListeners()},_cancelAnimation:function(){this.$.tooltip.classList.remove(this._getAnimationType("entry")),this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.add("hidden")},_onAnimationFinish:function(){this._showing&&(this.$.tooltip.classList.remove(this._getAnimationType("entry")),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.add(this._getAnimationType("exit")))},_onAnimationEnd:function(){this._animationPlaying=!1,this._showing||(this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.$.tooltip.classList.add("hidden"))},_getAnimationType:function(t){if("entry"===t&&""!==this.animationEntry)return this.animationEntry;if("exit"===t&&""!==this.animationExit)return this.animationExit;if(this.animationConfig[t]&&"string"==typeof this.animationConfig[t][0].name){if(this.animationConfig[t][0].timing&&this.animationConfig[t][0].timing.delay&&0!==this.animationConfig[t][0].timing.delay){var i=this.animationConfig[t][0].timing.delay;"entry"===t?this.updateStyles({"--paper-tooltip-delay-in":i+"ms"}):"exit"===t&&this.updateStyles({"--paper-tooltip-delay-out":i+"ms"})}return this.animationConfig[t][0].name}},_removeListeners:function(){this._target&&(this.unlisten(this._target,"mouseenter","show"),this.unlisten(this._target,"focus","show"),this.unlisten(this._target,"mouseleave","hide"),this.unlisten(this._target,"blur","hide"),this.unlisten(this._target,"tap","hide")),this.unlisten(this.$.tooltip,"animationend","_onAnimationEnd"),this.unlisten(this,"mouseenter","hide")}})},3239:(t,i,e)=>{function n(t){if(!t||"object"!=typeof t)return t;if("[object Date]"==Object.prototype.toString.call(t))return new Date(t.getTime());if(Array.isArray(t))return t.map(n);var i={};return Object.keys(t).forEach((function(e){i[e]=n(t[e])})),i}e.d(i,{Z:()=>n})},93217:(t,i,e)=>{e.d(i,{Ud:()=>u});const n=Symbol("Comlink.proxy"),o=Symbol("Comlink.endpoint"),a=Symbol("Comlink.releaseProxy"),s=Symbol("Comlink.finalizer"),r=Symbol("Comlink.thrown"),c=t=>"object"==typeof t&&null!==t||"function"==typeof t,l=new Map([["proxy",{canHandle:t=>c(t)&&t[n],serialize(t){const{port1:i,port2:e}=new MessageChannel;return d(t,i),[e,[e]]},deserialize:t=>(t.start(),u(t))}],["throw",{canHandle:t=>c(t)&&r in t,serialize({value:t}){let i;return i=t instanceof Error?{isError:!0,value:{message:t.message,name:t.name,stack:t.stack}}:{isError:!1,value:t},[i,[]]},deserialize(t){if(t.isError)throw Object.assign(new Error(t.value.message),t.value);throw t.value}}]]);function d(t,i=globalThis,e=["*"]){i.addEventListener("message",(function o(a){if(!a||!a.data)return;if(!function(t,i){for(const e of t){if(i===e||"*"===e)return!0;if(e instanceof RegExp&&e.test(i))return!0}return!1}(e,a.origin))return void console.warn(`Invalid origin '${a.origin}' for comlink proxy`);const{id:c,type:l,path:u}=Object.assign({path:[]},a.data),m=(a.data.argumentList||[]).map(w);let h;try{const i=u.slice(0,-1).reduce(((t,i)=>t[i]),t),e=u.reduce(((t,i)=>t[i]),t);switch(l){case"GET":h=e;break;case"SET":i[u.slice(-1)[0]]=w(a.data.value),h=!0;break;case"APPLY":h=e.apply(i,m);break;case"CONSTRUCT":h=function(t){return Object.assign(t,{[n]:!0})}(new e(...m));break;case"ENDPOINT":{const{port1:i,port2:e}=new MessageChannel;d(t,e),h=function(t,i){return v.set(t,i),t}(i,[i])}break;case"RELEASE":h=void 0;break;default:return}}catch(t){h={value:t,[r]:0}}Promise.resolve(h).catch((t=>({value:t,[r]:0}))).then((e=>{const[n,a]=_(e);i.postMessage(Object.assign(Object.assign({},n),{id:c}),a),"RELEASE"===l&&(i.removeEventListener("message",o),p(i),s in t&&"function"==typeof t[s]&&t[s]())})).catch((t=>{const[e,n]=_({value:new TypeError("Unserializable return value"),[r]:0});i.postMessage(Object.assign(Object.assign({},e),{id:c}),n)}))})),i.start&&i.start()}function p(t){(function(t){return"MessagePort"===t.constructor.name})(t)&&t.close()}function u(t,i){return g(t,[],i)}function m(t){if(t)throw new Error("Proxy has been released and is not useable")}function h(t){return x(t,{type:"RELEASE"}).then((()=>{p(t)}))}const f=new WeakMap,b="FinalizationRegistry"in globalThis&&new FinalizationRegistry((t=>{const i=(f.get(t)||0)-1;f.set(t,i),0===i&&h(t)}));function g(t,i=[],e=function(){}){let n=!1;const s=new Proxy(e,{get(e,o){if(m(n),o===a)return()=>{!function(t){b&&b.unregister(t)}(s),h(t),n=!0};if("then"===o){if(0===i.length)return{then:()=>s};const e=x(t,{type:"GET",path:i.map((t=>t.toString()))}).then(w);return e.then.bind(e)}return g(t,[...i,o])},set(e,o,a){m(n);const[s,r]=_(a);return x(t,{type:"SET",path:[...i,o].map((t=>t.toString())),value:s},r).then(w)},apply(e,a,s){m(n);const r=i[i.length-1];if(r===o)return x(t,{type:"ENDPOINT"}).then(w);if("bind"===r)return g(t,i.slice(0,-1));const[c,l]=y(s);return x(t,{type:"APPLY",path:i.map((t=>t.toString())),argumentList:c},l).then(w)},construct(e,o){m(n);const[a,s]=y(o);return x(t,{type:"CONSTRUCT",path:i.map((t=>t.toString())),argumentList:a},s).then(w)}});return function(t,i){const e=(f.get(i)||0)+1;f.set(i,e),b&&b.register(t,i,t)}(s,t),s}function y(t){const i=t.map(_);return[i.map((t=>t[0])),(e=i.map((t=>t[1])),Array.prototype.concat.apply([],e))];var e}const v=new WeakMap;function _(t){for(const[i,e]of l)if(e.canHandle(t)){const[n,o]=e.serialize(t);return[{type:"HANDLER",name:i,value:n},o]}return[{type:"RAW",value:t},v.get(t)||[]]}function w(t){switch(t.type){case"HANDLER":return l.get(t.name).deserialize(t.value);case"RAW":return t.value}}function x(t,i,e){return new Promise((n=>{const o=new Array(4).fill(0).map((()=>Math.floor(Math.random()*Number.MAX_SAFE_INTEGER).toString(16))).join("-");t.addEventListener("message",(function i(e){e.data&&e.data.id&&e.data.id===o&&(t.removeEventListener("message",i),n(e.data))})),t.start&&t.start(),t.postMessage(Object.assign({id:o},i),e)}))}},82160:(t,i,e)=>{function n(t){return new Promise(((i,e)=>{t.oncomplete=t.onsuccess=()=>i(t.result),t.onabort=t.onerror=()=>e(t.error)}))}function o(t,i){const e=indexedDB.open(t);e.onupgradeneeded=()=>e.result.createObjectStore(i);const o=n(e);return(t,e)=>o.then((n=>e(n.transaction(i,t).objectStore(i))))}let a;function s(){return a||(a=o("keyval-store","keyval")),a}function r(t,i=s()){return i("readonly",(i=>n(i.get(t))))}function c(t,i,e=s()){return e("readwrite",(e=>(e.put(i,t),n(e.transaction))))}function l(t=s()){return t("readwrite",(t=>(t.clear(),n(t.transaction))))}e.d(i,{MT:()=>o,RV:()=>n,U2:()=>r,ZH:()=>l,t8:()=>c})},19596:(t,i,e)=>{e.d(i,{sR:()=>p});var n=e(81563),o=e(38941);const a=(t,i)=>{var e,n;const o=t._$AN;if(void 0===o)return!1;for(const t of o)null===(n=(e=t)._$AO)||void 0===n||n.call(e,i,!1),a(t,i);return!0},s=t=>{let i,e;do{if(void 0===(i=t._$AM))break;e=i._$AN,e.delete(t),t=i}while(0===(null==e?void 0:e.size))},r=t=>{for(let i;i=t._$AM;t=i){let e=i._$AN;if(void 0===e)i._$AN=e=new Set;else if(e.has(t))break;e.add(t),d(i)}};function c(t){void 0!==this._$AN?(s(this),this._$AM=t,r(this)):this._$AM=t}function l(t,i=!1,e=0){const n=this._$AH,o=this._$AN;if(void 0!==o&&0!==o.size)if(i)if(Array.isArray(n))for(let t=e;t<n.length;t++)a(n[t],!1),s(n[t]);else null!=n&&(a(n,!1),s(n));else a(this,t)}const d=t=>{var i,e,n,a;t.type==o.pX.CHILD&&(null!==(i=(n=t)._$AP)&&void 0!==i||(n._$AP=l),null!==(e=(a=t)._$AQ)&&void 0!==e||(a._$AQ=c))};class p extends o.Xe{constructor(){super(...arguments),this._$AN=void 0}_$AT(t,i,e){super._$AT(t,i,e),r(this),this.isConnected=t._$AU}_$AO(t,i=!0){var e,n;t!==this.isConnected&&(this.isConnected=t,t?null===(e=this.reconnected)||void 0===e||e.call(this):null===(n=this.disconnected)||void 0===n||n.call(this)),i&&(a(this,t),s(this))}setValue(t){if((0,n.OR)(this._$Ct))this._$Ct._$AI(t,this);else{const i=[...this._$Ct._$AH];i[this._$Ci]=t,this._$Ct._$AI(i,this,0)}}disconnected(){}reconnected(){}}},81563:(t,i,e)=>{e.d(i,{E_:()=>b,OR:()=>c,_Y:()=>d,dZ:()=>r,fk:()=>p,hN:()=>s,hl:()=>m,i9:()=>h,pt:()=>a,ws:()=>f});var n=e(15304);const{I:o}=n._$LH,a=t=>null===t||"object"!=typeof t&&"function"!=typeof t,s=(t,i)=>void 0===i?void 0!==(null==t?void 0:t._$litType$):(null==t?void 0:t._$litType$)===i,r=t=>{var i;return null!=(null===(i=null==t?void 0:t._$litType$)||void 0===i?void 0:i.h)},c=t=>void 0===t.strings,l=()=>document.createComment(""),d=(t,i,e)=>{var n;const a=t._$AA.parentNode,s=void 0===i?t._$AB:i._$AA;if(void 0===e){const i=a.insertBefore(l(),s),n=a.insertBefore(l(),s);e=new o(i,n,t,t.options)}else{const i=e._$AB.nextSibling,o=e._$AM,r=o!==t;if(r){let i;null===(n=e._$AQ)||void 0===n||n.call(e,t),e._$AM=t,void 0!==e._$AP&&(i=t._$AU)!==o._$AU&&e._$AP(i)}if(i!==s||r){let t=e._$AA;for(;t!==i;){const i=t.nextSibling;a.insertBefore(t,s),t=i}}}return e},p=(t,i,e=t)=>(t._$AI(i,e),t),u={},m=(t,i=u)=>t._$AH=i,h=t=>t._$AH,f=t=>{var i;null===(i=t._$AP)||void 0===i||i.call(t,!1,!0);let e=t._$AA;const n=t._$AB.nextSibling;for(;e!==n;){const t=e.nextSibling;e.remove(),e=t}},b=t=>{t._$AR()}},57835:(t,i,e)=>{e.d(i,{XM:()=>n.XM,Xe:()=>n.Xe,pX:()=>n.pX});var n=e(38941)},47501:(t,i,e)=>{e.d(i,{V:()=>n.V});var n=e(84298)}};
//# sourceMappingURL=70790-PQilXb5gH-s.js.map