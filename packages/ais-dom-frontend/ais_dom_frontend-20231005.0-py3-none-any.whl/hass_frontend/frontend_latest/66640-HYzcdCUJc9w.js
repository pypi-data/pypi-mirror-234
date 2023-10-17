/*! For license information please see 66640-HYzcdCUJc9w.js.LICENSE.txt */
export const id=66640;export const ids=[66640];export const modules={54040:(e,t,i)=>{var o=i(87480),a=i(79932),n=i(58417),s=i(39274);let r=class extends n.A{};r.styles=[s.W],r=(0,o.__decorate)([(0,a.Mo)("mwc-checkbox")],r)},1819:(e,t,i)=>{var o=i(87480),a=i(79932),n=i(8485),s=i(92038);let r=class extends n.a{};r.styles=[s.W],r=(0,o.__decorate)([(0,a.Mo)("mwc-formfield")],r)},39841:(e,t,i)=>{i(56299),i(65660);var o=i(9672),a=i(69491),n=i(50856),s=i(44181);(0,o.k)({_template:n.d`
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
`,is:"app-header-layout",behaviors:[s.Y],properties:{hasScrollingRegion:{type:Boolean,value:!1,reflectToAttribute:!0}},observers:["resetLayout(isAttached, hasScrollingRegion)"],get header(){return(0,a.vz)(this.$.headerSlot).getDistributedNodes()[0]},_updateLayoutStates:function(){var e=this.header;if(this.isAttached&&e){this.$.wrapper.classList.remove("initializing"),e.scrollTarget=this.hasScrollingRegion?this.$.contentContainer:this.ownerDocument.documentElement;var t=e.offsetHeight;this.hasScrollingRegion?(e.style.left="",e.style.right=""):requestAnimationFrame(function(){var t=this.getBoundingClientRect(),i=document.documentElement.clientWidth-t.right;e.style.left=t.left+"px",e.style.right=i+"px"}.bind(this));var i=this.$.contentContainer.style;e.fixed&&!e.condenses&&this.hasScrollingRegion?(i.marginTop=t+"px",i.paddingTop=""):(i.paddingTop=t+"px",i.marginTop="")}}})},46628:(e,t,i)=>{i.d(t,{r:()=>o});const o={title:"AI-Speaker",views:[{badges:[],cards:[{entities:[{entity:"sensor.status_serwisu_zigbee2mqtt"},{entity:"sensor.wersja_zigbee2mqtt"},{entity:"sensor.wersja_kordynatora"},{type:"divider"},{entity:"switch.zigbee_tryb_parowania"},{entity:"timer.zigbee_permit_join"},{type:"divider"},{entity:"input_text.zigbee2mqtt_old_name"},{entity:"input_text.zigbee2mqtt_new_name"},{entity:"script.zigbee2mqtt_rename"},{type:"divider"},{entity:"input_text.zigbee2mqtt_remove"},{entity:"script.zigbee2mqtt_remove"}],show_header_toggle:!1,title:"Zigbee",type:"entities"},{entity:"sensor.zigbee2mqtt_networkmap",type:"ais-zigbee2mqtt"}],icon:"mdi:zigbee",path:"aiszigbee",title:"zigbee",visible:!1}]}},66640:(e,t,i)=>{i.a(e,(async(e,o)=>{try{i.r(t);var a=i(17463),n=i(34541),s=i(47838),r=i(68144),l=i(79932),d=(i(39841),i(27289),i(12730),i(54040),i(1819),i(48932),i(22098),i(46628)),h=i(11654),p=i(10009),c=e([p]);p=(c.then?(await c)():c)[0];(0,a.Z)([(0,l.Mo)("ha-panel-aiszigbee")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,l.Cb)()],key:"hass",value:void 0},{kind:"field",decorators:[(0,l.Cb)({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"_columns",value:void 0},{kind:"field",key:"mqls",value:void 0},{kind:"method",key:"_updateColumns",value:function(){const e=this.mqls.reduce(((e,t)=>e+Number(t.matches)),0);this._columns=Math.max(1,e-Number(!this.narrow&&"docked"===this.hass.dockedSidebar))}},{kind:"method",key:"updated",value:function(e){if((0,n.Z)((0,s.Z)(i.prototype),"updated",this).call(this,e),e.has("narrow"))return void this._updateColumns();if(!e.has("hass"))return;const t=e.get("hass");t&&this.hass.dockedSidebar!==t.dockedSidebar&&this._updateColumns()}},{kind:"method",key:"firstUpdated",value:function(){this._updateColumns=this._updateColumns.bind(this),this.mqls=[300,600,900,1200].map((e=>{const t=matchMedia(`(min-width: ${e}px)`);return t.addListener(this._updateColumns),t})),this._updateColumns()}},{kind:"method",key:"_showHelp",value:async function(){window.open("https://www.ai-speaker.com/docs/ais_app_integration_zigbee","_blank").focus()}},{kind:"method",key:"render",value:function(){const e={config:d.r,rawConfig:d.r,editMode:!1,urlPath:null,enableFullEditMode:()=>{},mode:"storage",locale:this.hass.locale,saveConfig:async()=>{},deleteConfig:async()=>{},setEditMode:()=>{}};return r.dy` <app-header-layout has-scrolling-region> <app-header fixed slot="header"> <app-toolbar> <ha-menu-button .hass="${this.hass}" .narrow="${this.narrow}"></ha-menu-button> <div main-title>Zigbee</div> <ha-icon-button label="Pomoc" icon="hass:information-outline" @click="${this._showHelp}"></ha-icon-button> </app-toolbar> </app-header> <hui-view .hass="${this.hass}" .lovelace="${e}" index="0" .columns="${this._columns}"></hui-view> </app-header-layout> `}},{kind:"get",static:!0,key:"styles",value:function(){return[h.Qx,r.iv`.content{padding:16px;display:flex;box-sizing:border-box}:host(:not([narrow])) .content{height:calc(100vh - 64px)}:host([narrow]) .content{flex-direction:column-reverse;padding:8px 0 0 0}:host([narrow]) .calendar-list{margin-bottom:24px;width:100%;padding-right:0}`]}}]}}),r.oi);o()}catch(e){o(e)}}))}};
//# sourceMappingURL=66640-HYzcdCUJc9w.js.map