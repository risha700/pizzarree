"use strict";(globalThis["webpackChunkpizzarree"]=globalThis["webpackChunkpizzarree"]||[]).push([[251],{4251:(e,s,a)=>{a.r(s),a.d(s,{default:()=>Q});a(2879);var t=a(9835),l=a(6970);const o={class:"q-pa-md q-gutter-sm"},r={class:"q-ml-sm"};function n(e,s,a,n,u,c){const i=(0,t.up)("q-avatar"),p=(0,t.up)("q-card-section"),m=(0,t.up)("q-btn"),d=(0,t.up)("q-card-actions"),g=(0,t.up)("q-card"),h=(0,t.up)("q-dialog"),v=(0,t.Q2)("close-popup");return(0,t.wg)(),(0,t.iD)("div",o,[(0,t.Wm)(h,{modelValue:n.hasMessage,"onUpdate:modelValue":s[1]||(s[1]=e=>n.hasMessage=e),persistent:""},{default:(0,t.w5)((()=>[(0,t.Wm)(g,null,{default:(0,t.w5)((()=>[(0,t.Wm)(p,{class:"items-center justify-center row",style:{"min-width":"30vw"}},{default:(0,t.w5)((()=>[(0,t.Wm)(i,{icon:"success"==n.level?"o_check_circle":"o_error_outline",color:"success"==n.level?"positive":"negative"},null,8,["icon","color"]),(0,t._)("span",r,(0,l.zw)(n.message),1)])),_:1}),(0,t.Wm)(d,{align:"right"},{default:(0,t.w5)((()=>[(0,t.wy)((0,t.Wm)(m,{flat:"",label:e.$t("dismiss"),onClick:s[0]||(s[0]=e=>n.router.push({name:"Home"}))},null,8,["label"]),[[v]])])),_:1})])),_:1})])),_:1},8,["modelValue"])])}var u=a(499),c=a(8339),i=a(6647);const p={name:"WebhookDone",setup(){const e=(0,c.tv)(),s=(0,c.yj)();let a=(0,u.ref)("Nothing to show!"),l=(0,u.ref)("");const{t:o}=(0,i.QT)(),r=(0,u.ref)(!0);return(0,t.bv)((async()=>{s.query.message||await e.push({name:"Home"}),a.value=s.query.message,l.value=s.query.level;let t=Object.assign({},s.query);delete t.message,delete t.level,await e.push({path:s.path})})),{message:a,level:l,router:e,t:o,hasMessage:r}}};var m=a(1639),d=a(2074),g=a(4458),h=a(3190),v=a(1357),w=a(1821),q=a(4455),f=a(2146),b=a(9984),y=a.n(b);const _=(0,m.Z)(p,[["render",n]]),Q=_;y()(p,"components",{QDialog:d.Z,QCard:g.Z,QCardSection:h.Z,QAvatar:v.Z,QCardActions:w.Z,QBtn:q.Z}),y()(p,"directives",{ClosePopup:f.Z})}}]);