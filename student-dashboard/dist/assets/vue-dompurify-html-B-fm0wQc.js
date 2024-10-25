/*! @license DOMPurify 3.1.7 | (c) Cure53 and other contributors | Released under the Apache license 2.0 and Mozilla Public License 2.0 | github.com/cure53/DOMPurify/blob/3.1.7/LICENSE */const{entries:dt,setPrototypeOf:rt,isFrozen:Gt,getPrototypeOf:Bt,getOwnPropertyDescriptor:Yt}=Object;let{freeze:A,seal:y,create:Tt}=Object,{apply:Ie,construct:Me}=typeof Reflect<"u"&&Reflect;A||(A=function(n){return n});y||(y=function(n){return n});Ie||(Ie=function(n,s,r){return n.apply(s,r)});Me||(Me=function(n,s){return new n(...s)});const le=L(Array.prototype.forEach),st=L(Array.prototype.pop),q=L(Array.prototype.push),fe=L(String.prototype.toLowerCase),Oe=L(String.prototype.toString),lt=L(String.prototype.match),K=L(String.prototype.replace),Xt=L(String.prototype.indexOf),jt=L(String.prototype.trim),O=L(Object.prototype.hasOwnProperty),h=L(RegExp.prototype.test),Z=Vt(TypeError);function L(a){return function(n){for(var s=arguments.length,r=new Array(s>1?s-1:0),f=1;f<s;f++)r[f-1]=arguments[f];return Ie(a,n,r)}}function Vt(a){return function(){for(var n=arguments.length,s=new Array(n),r=0;r<n;r++)s[r]=arguments[r];return Me(a,s)}}function l(a,n){let s=arguments.length>2&&arguments[2]!==void 0?arguments[2]:fe;rt&&rt(a,null);let r=n.length;for(;r--;){let f=n[r];if(typeof f=="string"){const R=s(f);R!==f&&(Gt(n)||(n[r]=R),f=R)}a[f]=!0}return a}function $t(a){for(let n=0;n<a.length;n++)O(a,n)||(a[n]=null);return a}function P(a){const n=Tt(null);for(const[s,r]of dt(a))O(a,s)&&(Array.isArray(r)?n[s]=$t(r):r&&typeof r=="object"&&r.constructor===Object?n[s]=P(r):n[s]=r);return n}function J(a,n){for(;a!==null;){const r=Yt(a,n);if(r){if(r.get)return L(r.get);if(typeof r.value=="function")return L(r.value)}a=Bt(a)}function s(){return null}return s}const ct=A(["a","abbr","acronym","address","area","article","aside","audio","b","bdi","bdo","big","blink","blockquote","body","br","button","canvas","caption","center","cite","code","col","colgroup","content","data","datalist","dd","decorator","del","details","dfn","dialog","dir","div","dl","dt","element","em","fieldset","figcaption","figure","font","footer","form","h1","h2","h3","h4","h5","h6","head","header","hgroup","hr","html","i","img","input","ins","kbd","label","legend","li","main","map","mark","marquee","menu","menuitem","meter","nav","nobr","ol","optgroup","option","output","p","picture","pre","progress","q","rp","rt","ruby","s","samp","section","select","shadow","small","source","spacer","span","strike","strong","style","sub","summary","sup","table","tbody","td","template","textarea","tfoot","th","thead","time","tr","track","tt","u","ul","var","video","wbr"]),De=A(["svg","a","altglyph","altglyphdef","altglyphitem","animatecolor","animatemotion","animatetransform","circle","clippath","defs","desc","ellipse","filter","font","g","glyph","glyphref","hkern","image","line","lineargradient","marker","mask","metadata","mpath","path","pattern","polygon","polyline","radialgradient","rect","stop","style","switch","symbol","text","textpath","title","tref","tspan","view","vkern"]),Ne=A(["feBlend","feColorMatrix","feComponentTransfer","feComposite","feConvolveMatrix","feDiffuseLighting","feDisplacementMap","feDistantLight","feDropShadow","feFlood","feFuncA","feFuncB","feFuncG","feFuncR","feGaussianBlur","feImage","feMerge","feMergeNode","feMorphology","feOffset","fePointLight","feSpecularLighting","feSpotLight","feTile","feTurbulence"]),qt=A(["animate","color-profile","cursor","discard","font-face","font-face-format","font-face-name","font-face-src","font-face-uri","foreignobject","hatch","hatchpath","mesh","meshgradient","meshpatch","meshrow","missing-glyph","script","set","solidcolor","unknown","use"]),be=A(["math","menclose","merror","mfenced","mfrac","mglyph","mi","mlabeledtr","mmultiscripts","mn","mo","mover","mpadded","mphantom","mroot","mrow","ms","mspace","msqrt","mstyle","msub","msup","msubsup","mtable","mtd","mtext","mtr","munder","munderover","mprescripts"]),Kt=A(["maction","maligngroup","malignmark","mlongdiv","mscarries","mscarry","msgroup","mstack","msline","msrow","semantics","annotation","annotation-xml","mprescripts","none"]),ft=A(["#text"]),ut=A(["accept","action","align","alt","autocapitalize","autocomplete","autopictureinpicture","autoplay","background","bgcolor","border","capture","cellpadding","cellspacing","checked","cite","class","clear","color","cols","colspan","controls","controlslist","coords","crossorigin","datetime","decoding","default","dir","disabled","disablepictureinpicture","disableremoteplayback","download","draggable","enctype","enterkeyhint","face","for","headers","height","hidden","high","href","hreflang","id","inputmode","integrity","ismap","kind","label","lang","list","loading","loop","low","max","maxlength","media","method","min","minlength","multiple","muted","name","nonce","noshade","novalidate","nowrap","open","optimum","pattern","placeholder","playsinline","popover","popovertarget","popovertargetaction","poster","preload","pubdate","radiogroup","readonly","rel","required","rev","reversed","role","rows","rowspan","spellcheck","scope","selected","shape","size","sizes","span","srclang","start","src","srcset","step","style","summary","tabindex","title","translate","type","usemap","valign","value","width","wrap","xmlns","slot"]),Ce=A(["accent-height","accumulate","additive","alignment-baseline","amplitude","ascent","attributename","attributetype","azimuth","basefrequency","baseline-shift","begin","bias","by","class","clip","clippathunits","clip-path","clip-rule","color","color-interpolation","color-interpolation-filters","color-profile","color-rendering","cx","cy","d","dx","dy","diffuseconstant","direction","display","divisor","dur","edgemode","elevation","end","exponent","fill","fill-opacity","fill-rule","filter","filterunits","flood-color","flood-opacity","font-family","font-size","font-size-adjust","font-stretch","font-style","font-variant","font-weight","fx","fy","g1","g2","glyph-name","glyphref","gradientunits","gradienttransform","height","href","id","image-rendering","in","in2","intercept","k","k1","k2","k3","k4","kerning","keypoints","keysplines","keytimes","lang","lengthadjust","letter-spacing","kernelmatrix","kernelunitlength","lighting-color","local","marker-end","marker-mid","marker-start","markerheight","markerunits","markerwidth","maskcontentunits","maskunits","max","mask","media","method","mode","min","name","numoctaves","offset","operator","opacity","order","orient","orientation","origin","overflow","paint-order","path","pathlength","patterncontentunits","patterntransform","patternunits","points","preservealpha","preserveaspectratio","primitiveunits","r","rx","ry","radius","refx","refy","repeatcount","repeatdur","restart","result","rotate","scale","seed","shape-rendering","slope","specularconstant","specularexponent","spreadmethod","startoffset","stddeviation","stitchtiles","stop-color","stop-opacity","stroke-dasharray","stroke-dashoffset","stroke-linecap","stroke-linejoin","stroke-miterlimit","stroke-opacity","stroke","stroke-width","style","surfacescale","systemlanguage","tabindex","tablevalues","targetx","targety","transform","transform-origin","text-anchor","text-decoration","text-rendering","textlength","type","u1","u2","unicode","values","viewbox","visibility","version","vert-adv-y","vert-origin-x","vert-origin-y","width","word-spacing","wrap","writing-mode","xchannelselector","ychannelselector","x","x1","x2","xmlns","y","y1","y2","z","zoomandpan"]),mt=A(["accent","accentunder","align","bevelled","close","columnsalign","columnlines","columnspan","denomalign","depth","dir","display","displaystyle","encoding","fence","frame","height","href","id","largeop","length","linethickness","lspace","lquote","mathbackground","mathcolor","mathsize","mathvariant","maxsize","minsize","movablelimits","notation","numalign","open","rowalign","rowlines","rowspacing","rowspan","rspace","rquote","scriptlevel","scriptminsize","scriptsizemultiplier","selection","separator","separators","stretchy","subscriptshift","supscriptshift","symmetric","voffset","width","xmlns"]),ce=A(["xlink:href","xml:id","xlink:title","xml:space","xmlns:xlink"]),Zt=y(/\{\{[\w\W]*|[\w\W]*\}\}/gm),Jt=y(/<%[\w\W]*|[\w\W]*%>/gm),Qt=y(/\${[\w\W]*}/gm),en=y(/^data-[\-\w.\u00B7-\uFFFF]/),tn=y(/^aria-[\-\w]+$/),_t=y(/^(?:(?:(?:f|ht)tps?|mailto|tel|callto|sms|cid|xmpp):|[^a-z]|[a-z+.\-]+(?:[^a-z+.\-:]|$))/i),nn=y(/^(?:\w+script|data):/i),on=y(/[\u0000-\u0020\u00A0\u1680\u180E\u2000-\u2029\u205F\u3000]/g),Et=y(/^html$/i),an=y(/^[a-z][.\w]*(-[.\w]+)+$/i);var pt=Object.freeze({__proto__:null,MUSTACHE_EXPR:Zt,ERB_EXPR:Jt,TMPLIT_EXPR:Qt,DATA_ATTR:en,ARIA_ATTR:tn,IS_ALLOWED_URI:_t,IS_SCRIPT_OR_DATA:nn,ATTR_WHITESPACE:on,DOCTYPE_NAME:Et,CUSTOM_ELEMENT:an});const Q={element:1,attribute:2,text:3,cdataSection:4,entityReference:5,entityNode:6,progressingInstruction:7,comment:8,document:9,documentType:10,documentFragment:11,notation:12},rn=function(){return typeof window>"u"?null:window},sn=function(n,s){if(typeof n!="object"||typeof n.createPolicy!="function")return null;let r=null;const f="data-tt-policy-suffix";s&&s.hasAttribute(f)&&(r=s.getAttribute(f));const R="dompurify"+(r?"#"+r:"");try{return n.createPolicy(R,{createHTML(C){return C},createScriptURL(C){return C}})}catch{return console.warn("TrustedTypes policy "+R+" could not be created."),null}};function gt(){let a=arguments.length>0&&arguments[0]!==void 0?arguments[0]:rn();const n=i=>gt(i);if(n.version="3.1.7",n.removed=[],!a||!a.document||a.document.nodeType!==Q.document)return n.isSupported=!1,n;let{document:s}=a;const r=s,f=r.currentScript,{DocumentFragment:R,HTMLTemplateElement:C,Node:v,Element:G,NodeFilter:w,NamedNodeMap:ee=a.NamedNodeMap||a.MozNamedAttrMap,HTMLFormElement:At,DOMParser:St,trustedTypes:te}=a,B=G.prototype,Rt=J(B,"cloneNode"),Lt=J(B,"remove"),yt=J(B,"nextSibling"),Ot=J(B,"childNodes"),ne=J(B,"parentNode");if(typeof C=="function"){const i=s.createElement("template");i.content&&i.content.ownerDocument&&(s=i.content.ownerDocument)}let E,Y="";const{implementation:ue,createNodeIterator:Dt,createDocumentFragment:Nt,getElementsByTagName:bt}=s,{importNode:Ct}=r;let D={};n.isSupported=typeof dt=="function"&&typeof ne=="function"&&ue&&ue.createHTMLDocument!==void 0;const{MUSTACHE_EXPR:me,ERB_EXPR:pe,TMPLIT_EXPR:de,DATA_ATTR:It,ARIA_ATTR:Mt,IS_SCRIPT_OR_DATA:wt,ATTR_WHITESPACE:we,CUSTOM_ELEMENT:xt}=pt;let{IS_ALLOWED_URI:xe}=pt,m=null;const Pe=l({},[...ct,...De,...Ne,...be,...ft]);let p=null;const ve=l({},[...ut,...Ce,...mt,...ce]);let u=Object.seal(Tt(null,{tagNameCheck:{writable:!0,configurable:!1,enumerable:!0,value:null},attributeNameCheck:{writable:!0,configurable:!1,enumerable:!0,value:null},allowCustomizedBuiltInElements:{writable:!0,configurable:!1,enumerable:!0,value:!1}})),X=null,Te=null,ke=!0,_e=!0,Ue=!1,Fe=!0,k=!1,Ee=!0,x=!1,ge=!1,he=!1,U=!1,oe=!1,ie=!1,He=!0,ze=!1;const Pt="user-content-";let Ae=!0,j=!1,F={},H=null;const We=l({},["annotation-xml","audio","colgroup","desc","foreignobject","head","iframe","math","mi","mn","mo","ms","mtext","noembed","noframes","noscript","plaintext","script","style","svg","template","thead","title","video","xmp"]);let Ge=null;const Be=l({},["audio","video","img","source","image","track"]);let Se=null;const Ye=l({},["alt","class","for","id","label","name","pattern","placeholder","role","summary","title","value","style","xmlns"]),ae="http://www.w3.org/1998/Math/MathML",re="http://www.w3.org/2000/svg",I="http://www.w3.org/1999/xhtml";let z=I,Re=!1,Le=null;const vt=l({},[ae,re,I],Oe);let V=null;const kt=["application/xhtml+xml","text/html"],Ut="text/html";let d=null,W=null;const Ft=s.createElement("form"),Xe=function(e){return e instanceof RegExp||e instanceof Function},ye=function(){let e=arguments.length>0&&arguments[0]!==void 0?arguments[0]:{};if(!(W&&W===e)){if((!e||typeof e!="object")&&(e={}),e=P(e),V=kt.indexOf(e.PARSER_MEDIA_TYPE)===-1?Ut:e.PARSER_MEDIA_TYPE,d=V==="application/xhtml+xml"?Oe:fe,m=O(e,"ALLOWED_TAGS")?l({},e.ALLOWED_TAGS,d):Pe,p=O(e,"ALLOWED_ATTR")?l({},e.ALLOWED_ATTR,d):ve,Le=O(e,"ALLOWED_NAMESPACES")?l({},e.ALLOWED_NAMESPACES,Oe):vt,Se=O(e,"ADD_URI_SAFE_ATTR")?l(P(Ye),e.ADD_URI_SAFE_ATTR,d):Ye,Ge=O(e,"ADD_DATA_URI_TAGS")?l(P(Be),e.ADD_DATA_URI_TAGS,d):Be,H=O(e,"FORBID_CONTENTS")?l({},e.FORBID_CONTENTS,d):We,X=O(e,"FORBID_TAGS")?l({},e.FORBID_TAGS,d):{},Te=O(e,"FORBID_ATTR")?l({},e.FORBID_ATTR,d):{},F=O(e,"USE_PROFILES")?e.USE_PROFILES:!1,ke=e.ALLOW_ARIA_ATTR!==!1,_e=e.ALLOW_DATA_ATTR!==!1,Ue=e.ALLOW_UNKNOWN_PROTOCOLS||!1,Fe=e.ALLOW_SELF_CLOSE_IN_ATTR!==!1,k=e.SAFE_FOR_TEMPLATES||!1,Ee=e.SAFE_FOR_XML!==!1,x=e.WHOLE_DOCUMENT||!1,U=e.RETURN_DOM||!1,oe=e.RETURN_DOM_FRAGMENT||!1,ie=e.RETURN_TRUSTED_TYPE||!1,he=e.FORCE_BODY||!1,He=e.SANITIZE_DOM!==!1,ze=e.SANITIZE_NAMED_PROPS||!1,Ae=e.KEEP_CONTENT!==!1,j=e.IN_PLACE||!1,xe=e.ALLOWED_URI_REGEXP||_t,z=e.NAMESPACE||I,u=e.CUSTOM_ELEMENT_HANDLING||{},e.CUSTOM_ELEMENT_HANDLING&&Xe(e.CUSTOM_ELEMENT_HANDLING.tagNameCheck)&&(u.tagNameCheck=e.CUSTOM_ELEMENT_HANDLING.tagNameCheck),e.CUSTOM_ELEMENT_HANDLING&&Xe(e.CUSTOM_ELEMENT_HANDLING.attributeNameCheck)&&(u.attributeNameCheck=e.CUSTOM_ELEMENT_HANDLING.attributeNameCheck),e.CUSTOM_ELEMENT_HANDLING&&typeof e.CUSTOM_ELEMENT_HANDLING.allowCustomizedBuiltInElements=="boolean"&&(u.allowCustomizedBuiltInElements=e.CUSTOM_ELEMENT_HANDLING.allowCustomizedBuiltInElements),k&&(_e=!1),oe&&(U=!0),F&&(m=l({},ft),p=[],F.html===!0&&(l(m,ct),l(p,ut)),F.svg===!0&&(l(m,De),l(p,Ce),l(p,ce)),F.svgFilters===!0&&(l(m,Ne),l(p,Ce),l(p,ce)),F.mathMl===!0&&(l(m,be),l(p,mt),l(p,ce))),e.ADD_TAGS&&(m===Pe&&(m=P(m)),l(m,e.ADD_TAGS,d)),e.ADD_ATTR&&(p===ve&&(p=P(p)),l(p,e.ADD_ATTR,d)),e.ADD_URI_SAFE_ATTR&&l(Se,e.ADD_URI_SAFE_ATTR,d),e.FORBID_CONTENTS&&(H===We&&(H=P(H)),l(H,e.FORBID_CONTENTS,d)),Ae&&(m["#text"]=!0),x&&l(m,["html","head","body"]),m.table&&(l(m,["tbody"]),delete X.tbody),e.TRUSTED_TYPES_POLICY){if(typeof e.TRUSTED_TYPES_POLICY.createHTML!="function")throw Z('TRUSTED_TYPES_POLICY configuration option must provide a "createHTML" hook.');if(typeof e.TRUSTED_TYPES_POLICY.createScriptURL!="function")throw Z('TRUSTED_TYPES_POLICY configuration option must provide a "createScriptURL" hook.');E=e.TRUSTED_TYPES_POLICY,Y=E.createHTML("")}else E===void 0&&(E=sn(te,f)),E!==null&&typeof Y=="string"&&(Y=E.createHTML(""));A&&A(e),W=e}},je=l({},["mi","mo","mn","ms","mtext"]),Ve=l({},["annotation-xml"]),Ht=l({},["title","style","font","a","script"]),$e=l({},[...De,...Ne,...qt]),qe=l({},[...be,...Kt]),zt=function(e){let t=ne(e);(!t||!t.tagName)&&(t={namespaceURI:z,tagName:"template"});const o=fe(e.tagName),c=fe(t.tagName);return Le[e.namespaceURI]?e.namespaceURI===re?t.namespaceURI===I?o==="svg":t.namespaceURI===ae?o==="svg"&&(c==="annotation-xml"||je[c]):!!$e[o]:e.namespaceURI===ae?t.namespaceURI===I?o==="math":t.namespaceURI===re?o==="math"&&Ve[c]:!!qe[o]:e.namespaceURI===I?t.namespaceURI===re&&!Ve[c]||t.namespaceURI===ae&&!je[c]?!1:!qe[o]&&(Ht[o]||!$e[o]):!!(V==="application/xhtml+xml"&&Le[e.namespaceURI]):!1},N=function(e){q(n.removed,{element:e});try{ne(e).removeChild(e)}catch{Lt(e)}},se=function(e,t){try{q(n.removed,{attribute:t.getAttributeNode(e),from:t})}catch{q(n.removed,{attribute:null,from:t})}if(t.removeAttribute(e),e==="is"&&!p[e])if(U||oe)try{N(t)}catch{}else try{t.setAttribute(e,"")}catch{}},Ke=function(e){let t=null,o=null;if(he)e="<remove></remove>"+e;else{const T=lt(e,/^[\r\n\t ]+/);o=T&&T[0]}V==="application/xhtml+xml"&&z===I&&(e='<html xmlns="http://www.w3.org/1999/xhtml"><head></head><body>'+e+"</body></html>");const c=E?E.createHTML(e):e;if(z===I)try{t=new St().parseFromString(c,V)}catch{}if(!t||!t.documentElement){t=ue.createDocument(z,"template",null);try{t.documentElement.innerHTML=Re?Y:c}catch{}}const _=t.body||t.documentElement;return e&&o&&_.insertBefore(s.createTextNode(o),_.childNodes[0]||null),z===I?bt.call(t,x?"html":"body")[0]:x?t.documentElement:_},Ze=function(e){return Dt.call(e.ownerDocument||e,e,w.SHOW_ELEMENT|w.SHOW_COMMENT|w.SHOW_TEXT|w.SHOW_PROCESSING_INSTRUCTION|w.SHOW_CDATA_SECTION,null)},Je=function(e){return e instanceof At&&(typeof e.nodeName!="string"||typeof e.textContent!="string"||typeof e.removeChild!="function"||!(e.attributes instanceof ee)||typeof e.removeAttribute!="function"||typeof e.setAttribute!="function"||typeof e.namespaceURI!="string"||typeof e.insertBefore!="function"||typeof e.hasChildNodes!="function")},Qe=function(e){return typeof v=="function"&&e instanceof v},M=function(e,t,o){D[e]&&le(D[e],c=>{c.call(n,t,o,W)})},et=function(e){let t=null;if(M("beforeSanitizeElements",e,null),Je(e))return N(e),!0;const o=d(e.nodeName);if(M("uponSanitizeElement",e,{tagName:o,allowedTags:m}),e.hasChildNodes()&&!Qe(e.firstElementChild)&&h(/<[/\w]/g,e.innerHTML)&&h(/<[/\w]/g,e.textContent)||e.nodeType===Q.progressingInstruction||Ee&&e.nodeType===Q.comment&&h(/<[/\w]/g,e.data))return N(e),!0;if(!m[o]||X[o]){if(!X[o]&&nt(o)&&(u.tagNameCheck instanceof RegExp&&h(u.tagNameCheck,o)||u.tagNameCheck instanceof Function&&u.tagNameCheck(o)))return!1;if(Ae&&!H[o]){const c=ne(e)||e.parentNode,_=Ot(e)||e.childNodes;if(_&&c){const T=_.length;for(let S=T-1;S>=0;--S){const b=Rt(_[S],!0);b.__removalCount=(e.__removalCount||0)+1,c.insertBefore(b,yt(e))}}}return N(e),!0}return e instanceof G&&!zt(e)||(o==="noscript"||o==="noembed"||o==="noframes")&&h(/<\/no(script|embed|frames)/i,e.innerHTML)?(N(e),!0):(k&&e.nodeType===Q.text&&(t=e.textContent,le([me,pe,de],c=>{t=K(t,c," ")}),e.textContent!==t&&(q(n.removed,{element:e.cloneNode()}),e.textContent=t)),M("afterSanitizeElements",e,null),!1)},tt=function(e,t,o){if(He&&(t==="id"||t==="name")&&(o in s||o in Ft))return!1;if(!(_e&&!Te[t]&&h(It,t))){if(!(ke&&h(Mt,t))){if(!p[t]||Te[t]){if(!(nt(e)&&(u.tagNameCheck instanceof RegExp&&h(u.tagNameCheck,e)||u.tagNameCheck instanceof Function&&u.tagNameCheck(e))&&(u.attributeNameCheck instanceof RegExp&&h(u.attributeNameCheck,t)||u.attributeNameCheck instanceof Function&&u.attributeNameCheck(t))||t==="is"&&u.allowCustomizedBuiltInElements&&(u.tagNameCheck instanceof RegExp&&h(u.tagNameCheck,o)||u.tagNameCheck instanceof Function&&u.tagNameCheck(o))))return!1}else if(!Se[t]){if(!h(xe,K(o,we,""))){if(!((t==="src"||t==="xlink:href"||t==="href")&&e!=="script"&&Xt(o,"data:")===0&&Ge[e])){if(!(Ue&&!h(wt,K(o,we,"")))){if(o)return!1}}}}}}return!0},nt=function(e){return e!=="annotation-xml"&&lt(e,xt)},ot=function(e){M("beforeSanitizeAttributes",e,null);const{attributes:t}=e;if(!t)return;const o={attrName:"",attrValue:"",keepAttr:!0,allowedAttributes:p};let c=t.length;for(;c--;){const _=t[c],{name:T,namespaceURI:S,value:b}=_,$=d(T);let g=T==="value"?b:jt(b);if(o.attrName=$,o.attrValue=g,o.keepAttr=!0,o.forceKeepAttr=void 0,M("uponSanitizeAttribute",e,o),g=o.attrValue,o.forceKeepAttr||(se(T,e),!o.keepAttr))continue;if(!Fe&&h(/\/>/i,g)){se(T,e);continue}k&&le([me,pe,de],at=>{g=K(g,at," ")});const it=d(e.nodeName);if(tt(it,$,g)){if(ze&&($==="id"||$==="name")&&(se(T,e),g=Pt+g),Ee&&h(/((--!?|])>)|<\/(style|title)/i,g)){se(T,e);continue}if(E&&typeof te=="object"&&typeof te.getAttributeType=="function"&&!S)switch(te.getAttributeType(it,$)){case"TrustedHTML":{g=E.createHTML(g);break}case"TrustedScriptURL":{g=E.createScriptURL(g);break}}try{S?e.setAttributeNS(S,T,g):e.setAttribute(T,g),Je(e)?N(e):st(n.removed)}catch{}}}M("afterSanitizeAttributes",e,null)},Wt=function i(e){let t=null;const o=Ze(e);for(M("beforeSanitizeShadowDOM",e,null);t=o.nextNode();)M("uponSanitizeShadowNode",t,null),!et(t)&&(t.content instanceof R&&i(t.content),ot(t));M("afterSanitizeShadowDOM",e,null)};return n.sanitize=function(i){let e=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},t=null,o=null,c=null,_=null;if(Re=!i,Re&&(i="<!-->"),typeof i!="string"&&!Qe(i))if(typeof i.toString=="function"){if(i=i.toString(),typeof i!="string")throw Z("dirty is not a string, aborting")}else throw Z("toString is not a function");if(!n.isSupported)return i;if(ge||ye(e),n.removed=[],typeof i=="string"&&(j=!1),j){if(i.nodeName){const b=d(i.nodeName);if(!m[b]||X[b])throw Z("root node is forbidden and cannot be sanitized in-place")}}else if(i instanceof v)t=Ke("<!---->"),o=t.ownerDocument.importNode(i,!0),o.nodeType===Q.element&&o.nodeName==="BODY"||o.nodeName==="HTML"?t=o:t.appendChild(o);else{if(!U&&!k&&!x&&i.indexOf("<")===-1)return E&&ie?E.createHTML(i):i;if(t=Ke(i),!t)return U?null:ie?Y:""}t&&he&&N(t.firstChild);const T=Ze(j?i:t);for(;c=T.nextNode();)et(c)||(c.content instanceof R&&Wt(c.content),ot(c));if(j)return i;if(U){if(oe)for(_=Nt.call(t.ownerDocument);t.firstChild;)_.appendChild(t.firstChild);else _=t;return(p.shadowroot||p.shadowrootmode)&&(_=Ct.call(r,_,!0)),_}let S=x?t.outerHTML:t.innerHTML;return x&&m["!doctype"]&&t.ownerDocument&&t.ownerDocument.doctype&&t.ownerDocument.doctype.name&&h(Et,t.ownerDocument.doctype.name)&&(S="<!DOCTYPE "+t.ownerDocument.doctype.name+`>
`+S),k&&le([me,pe,de],b=>{S=K(S,b," ")}),E&&ie?E.createHTML(S):S},n.setConfig=function(){let i=arguments.length>0&&arguments[0]!==void 0?arguments[0]:{};ye(i),ge=!0},n.clearConfig=function(){W=null,ge=!1},n.isValidAttribute=function(i,e,t){W||ye({});const o=d(i),c=d(e);return tt(o,c,t)},n.addHook=function(i,e){typeof e=="function"&&(D[i]=D[i]||[],q(D[i],e))},n.removeHook=function(i){if(D[i])return st(D[i])},n.removeHooks=function(i){D[i]&&(D[i]=[])},n.removeAllHooks=function(){D={}},n}var ln=gt();function cn(a,n){const s=a.hooks??{};let r;for(r in s){const f=s[r];f!==void 0&&n.addHook(r,f)}}function ht(){return ln()}function fn(a={},n=ht){const s=n();cn(a,s);const r=function(f,R){const C=R.value;if(R.oldValue===C)return;const v=`${C}`,G=R.arg,w=a.namedConfigurations,ee=a.default??{};if(w&&G!==void 0){f.innerHTML=s.sanitize(v,w[G]??ee);return}f.innerHTML=s.sanitize(v,ee)};return{mounted:r,updated:r}}const un={install(a,n={},s=ht){a.directive("dompurify-html",fn(n,s))}};export{un as k};