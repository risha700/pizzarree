"use strict";(globalThis["webpackChunkpizzarree"]=globalThis["webpackChunkpizzarree"]||[]).push([[321],{9321:(t,o,a)=>{a.r(o),a.d(o,{default:()=>T});var e=a(9835),d=a(6970);const r={key:0},c={class:"col-md-1"},u={class:"text-capitalize"},n={class:"flex tw-gap-4 justify-md-start"};function s(t,o,a,s,l,i){const p=(0,e.up)("ProductCard"),h=(0,e.up)("ProductModal");return t.products&&t.products.length?((0,e.wg)(),(0,e.iD)("div",r,[(0,e._)("div",c,[(0,e._)("h6",u,(0,d.zw)(t.header_title),1)]),(0,e._)("div",n,[((0,e.wg)(!0),(0,e.iD)(e.HY,null,(0,e.Ko)(t.products,(o=>((0,e.wg)(),(0,e.j4)(p,{key:o.id,product:o,onShowModal:t.showProductDetails},null,8,["product","onShowModal"])))),128))]),(0,e.Wm)(h,{"model-value":t.showModal,product:t.chosenProduct,onHideModal:t.hideHandler},null,8,["model-value","product","onHideModal"])])):(0,e.kq)("",!0)}var l=a(499);const i={class:"text-h6"},p={class:"text-subtitle2"};function h(t,o,a,r,c,u){const n=(0,e.up)("q-img"),s=(0,e.up)("q-card-section"),l=(0,e.up)("q-btn"),h=(0,e.up)("q-card-actions"),m=(0,e.up)("q-card");return t.product?((0,e.wg)(),(0,e.j4)(m,{key:0,class:"my-card"},{default:(0,e.w5)((()=>[(0,e.Wm)(n,{src:t.product.cover_image,height:"100px",onClick:o[0]||(o[0]=o=>t.handleCustomize(t.product))},null,8,["src"]),(0,e.Wm)(s,{class:""},{default:(0,e.w5)((()=>[(0,e._)("div",i,(0,d.zw)(t.product.name),1),(0,e._)("div",p,"$"+(0,d.zw)(t.product.price),1)])),_:1}),(0,e.Wm)(h,{align:"around"},{default:(0,e.w5)((()=>[(0,e.Wm)(l,{flat:"",onClick:o[1]||(o[1]=o=>t.straightToCart(t.product))},{default:(0,e.w5)((()=>[(0,e.Uk)("Add To Cart")])),_:1}),(0,e.Wm)(l,{onClick:o[2]||(o[2]=o=>t.handleCustomize(t.product)),flat:""},{default:(0,e.w5)((()=>[(0,e.Uk)("Customize")])),_:1})])),_:1})])),_:1})):(0,e.kq)("",!0)}var m=a(9524);const w=(0,e.aZ)({name:"ProductCard",props:["product"],emits:["showModal"],setup(t,{emit:o}){const a=(0,m.M)(),e=t=>{o("showModal",t)};async function d(e){if(e.tags.includes("pizza"))return void o("showModal",e);let d=t.product.tags[0]+"_"+(Math.random()+1).toString(36).substring(7);await a.addToLocalCart(d,[e])}return{handleCustomize:e,straightToCart:d}}});var C=a(1639),g=a(4458),f=a(335),v=a(3190),k=a(1821),z=a(4455),M=a(9984),_=a.n(M);const Z=(0,C.Z)(w,[["render",h]]),P=Z;_()(w,"components",{QCard:g.Z,QImg:f.Z,QCardSection:v.Z,QCardActions:k.Z,QBtn:z.Z});var b=a(6002);const q=(0,e.aZ)({name:"MenuComponent",methods:{capitalize:d.kC},components:{ProductModal:b.Z,ProductCard:P},props:["products","header_title"],async setup(){let t=(0,l.ref)(!1),o=(0,l.ref)({});function a(a){t.value=!0,o.value=a}function e(a){t.value=a,o.value={}}return{showProductDetails:a,showModal:t,chosenProduct:o,hideHandler:e}}}),y=(0,C.Z)(q,[["render",s]]),T=y}}]);