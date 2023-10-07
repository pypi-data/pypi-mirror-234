/*
 Highcharts JS v11.1.0 (2023-06-05)

 (c) 2016-2021 Highsoft AS
 Authors: Jon Arild Nygard

 License: www.highcharts.com/license
*/
'use strict';var $jscomp=$jscomp||{};$jscomp.scope={};$jscomp.arrayIteratorImpl=function(a){var c=0;return function(){return c<a.length?{done:!1,value:a[c++]}:{done:!0}}};$jscomp.arrayIterator=function(a){return{next:$jscomp.arrayIteratorImpl(a)}};$jscomp.ASSUME_ES5=!1;$jscomp.ASSUME_NO_NATIVE_MAP=!1;$jscomp.ASSUME_NO_NATIVE_SET=!1;$jscomp.SIMPLE_FROUND_POLYFILL=!1;$jscomp.ISOLATE_POLYFILLS=!1;
$jscomp.defineProperty=$jscomp.ASSUME_ES5||"function"==typeof Object.defineProperties?Object.defineProperty:function(a,c,b){if(a==Array.prototype||a==Object.prototype)return a;a[c]=b.value;return a};$jscomp.getGlobal=function(a){a=["object"==typeof globalThis&&globalThis,a,"object"==typeof window&&window,"object"==typeof self&&self,"object"==typeof global&&global];for(var c=0;c<a.length;++c){var b=a[c];if(b&&b.Math==Math)return b}throw Error("Cannot find global object");};$jscomp.global=$jscomp.getGlobal(this);
$jscomp.SYMBOL_PREFIX="jscomp_symbol_";$jscomp.initSymbol=function(){$jscomp.initSymbol=function(){};$jscomp.global.Symbol||($jscomp.global.Symbol=$jscomp.Symbol)};$jscomp.SymbolClass=function(a,c){this.$jscomp$symbol$id_=a;$jscomp.defineProperty(this,"description",{configurable:!0,writable:!0,value:c})};$jscomp.SymbolClass.prototype.toString=function(){return this.$jscomp$symbol$id_};
$jscomp.Symbol=function(){function a(b){if(this instanceof a)throw new TypeError("Symbol is not a constructor");return new $jscomp.SymbolClass($jscomp.SYMBOL_PREFIX+(b||"")+"_"+c++,b)}var c=0;return a}();
$jscomp.initSymbolIterator=function(){$jscomp.initSymbol();var a=$jscomp.global.Symbol.iterator;a||(a=$jscomp.global.Symbol.iterator=$jscomp.global.Symbol("Symbol.iterator"));"function"!=typeof Array.prototype[a]&&$jscomp.defineProperty(Array.prototype,a,{configurable:!0,writable:!0,value:function(){return $jscomp.iteratorPrototype($jscomp.arrayIteratorImpl(this))}});$jscomp.initSymbolIterator=function(){}};
$jscomp.initSymbolAsyncIterator=function(){$jscomp.initSymbol();var a=$jscomp.global.Symbol.asyncIterator;a||(a=$jscomp.global.Symbol.asyncIterator=$jscomp.global.Symbol("Symbol.asyncIterator"));$jscomp.initSymbolAsyncIterator=function(){}};$jscomp.iteratorPrototype=function(a){$jscomp.initSymbolIterator();a={next:a};a[$jscomp.global.Symbol.iterator]=function(){return this};return a};
$jscomp.iteratorFromArray=function(a,c){$jscomp.initSymbolIterator();a instanceof String&&(a+="");var b=0,d={next:function(){if(b<a.length){var e=b++;return{value:c(e,a[e]),done:!1}}d.next=function(){return{done:!0,value:void 0}};return d.next()}};d[Symbol.iterator]=function(){return d};return d};$jscomp.polyfills={};$jscomp.propertyToPolyfillSymbol={};$jscomp.POLYFILL_PREFIX="$jscp$";$jscomp.IS_SYMBOL_NATIVE="function"===typeof Symbol&&"symbol"===typeof Symbol("x");
var $jscomp$lookupPolyfilledValue=function(a,c){var b=$jscomp.propertyToPolyfillSymbol[c];if(null==b)return a[c];b=a[b];return void 0!==b?b:a[c]};$jscomp.polyfill=function(a,c,b,d){c&&($jscomp.ISOLATE_POLYFILLS?$jscomp.polyfillIsolated(a,c,b,d):$jscomp.polyfillUnisolated(a,c,b,d))};
$jscomp.polyfillUnisolated=function(a,c,b,d){b=$jscomp.global;a=a.split(".");for(d=0;d<a.length-1;d++){var e=a[d];e in b||(b[e]={});b=b[e]}a=a[a.length-1];d=b[a];c=c(d);c!=d&&null!=c&&$jscomp.defineProperty(b,a,{configurable:!0,writable:!0,value:c})};
$jscomp.polyfillIsolated=function(a,c,b,d){var e=a.split(".");a=1===e.length;d=e[0];d=!a&&d in $jscomp.polyfills?$jscomp.polyfills:$jscomp.global;for(var B=0;B<e.length-1;B++){var r=e[B];r in d||(d[r]={});d=d[r]}e=e[e.length-1];b=$jscomp.IS_SYMBOL_NATIVE&&"es6"===b?d[e]:null;c=c(b);null!=c&&(a?$jscomp.defineProperty($jscomp.polyfills,e,{configurable:!0,writable:!0,value:c}):c!==b&&($jscomp.propertyToPolyfillSymbol[e]=$jscomp.IS_SYMBOL_NATIVE?$jscomp.global.Symbol(e):$jscomp.POLYFILL_PREFIX+e,e=$jscomp.propertyToPolyfillSymbol[e],
$jscomp.defineProperty(d,e,{configurable:!0,writable:!0,value:c})))};$jscomp.polyfill("Array.prototype.values",function(a){return a?a:function(){return $jscomp.iteratorFromArray(this,function(a,b){return b})}},"es8","es3");
(function(a){"object"===typeof module&&module.exports?(a["default"]=a,module.exports=a):"function"===typeof define&&define.amd?define("highcharts/modules/sunburst",["highcharts"],function(c){a(c);a.Highcharts=c;return a}):a("undefined"!==typeof Highcharts?Highcharts:void 0)})(function(a){function c(a,d,e,c){a.hasOwnProperty(d)||(a[d]=c.apply(null,e),"function"===typeof CustomEvent&&window.dispatchEvent(new CustomEvent("HighchartsModuleLoaded",{detail:{path:d,module:a[d]}})))}a=a?a._modules:{};c(a,
"Series/ColorMapComposition.js",[a["Core/Series/SeriesRegistry.js"],a["Core/Utilities.js"]],function(a,d){const {column:{prototype:b}}=a.seriesTypes,{addEvent:c,defined:r}=d;var p;(function(a){function e(a){this.moveToTopOnHover&&this.graphic&&this.graphic.attr({zIndex:a&&"hover"===a.state?1:0})}const k=[];a.pointMembers={dataLabelOnNull:!0,moveToTopOnHover:!0,isValid:function(){return null!==this.value&&Infinity!==this.value&&-Infinity!==this.value&&(void 0===this.value||!isNaN(this.value))}};a.seriesMembers=
{colorKey:"value",axisTypes:["xAxis","yAxis","colorAxis"],parallelArrays:["x","y","value"],pointArrayMap:["value"],trackerGroups:["group","markerGroup","dataLabelsGroup"],colorAttribs:function(a){const f={};!r(a.color)||a.state&&"normal"!==a.state||(f[this.colorProp||"fill"]=a.color);return f},pointAttribs:b.pointAttribs};a.compose=function(a){const f=a.prototype.pointClass;d.pushUnique(k,f)&&c(f,"afterSetState",e);return a}})(p||(p={}));return p});c(a,"Series/Treemap/TreemapAlgorithmGroup.js",[],
function(){class a{constructor(a,b,c,r){this.height=a;this.width=b;this.plot=r;this.startDirection=this.direction=c;this.lH=this.nH=this.lW=this.nW=this.total=0;this.elArr=[];this.lP={total:0,lH:0,nH:0,lW:0,nW:0,nR:0,lR:0,aspectRatio:function(a,d){return Math.max(a/d,d/a)}}}addElement(a){this.lP.total=this.elArr[this.elArr.length-1];this.total+=a;0===this.direction?(this.lW=this.nW,this.lP.lH=this.lP.total/this.lW,this.lP.lR=this.lP.aspectRatio(this.lW,this.lP.lH),this.nW=this.total/this.height,this.lP.nH=
this.lP.total/this.nW,this.lP.nR=this.lP.aspectRatio(this.nW,this.lP.nH)):(this.lH=this.nH,this.lP.lW=this.lP.total/this.lH,this.lP.lR=this.lP.aspectRatio(this.lP.lW,this.lH),this.nH=this.total/this.width,this.lP.nW=this.lP.total/this.nH,this.lP.nR=this.lP.aspectRatio(this.lP.nW,this.nH));this.elArr.push(a)}reset(){this.lW=this.nW=0;this.elArr=[];this.total=0}}return a});c(a,"Series/DrawPointUtilities.js",[a["Core/Utilities.js"]],function(a){return{draw:function(a,b){const {animatableAttribs:d,onComplete:c,
css:e,renderer:k}=b,m=a.series&&a.series.chart.hasRendered?void 0:a.series&&a.series.options.animation;let t=a.graphic;b.attribs=Object.assign(Object.assign({},b.attribs),{"class":a.getClassName()})||{};if(a.shouldDraw())t||(a.graphic=t="text"===b.shapeType?k.text():k[b.shapeType](b.shapeArgs||{}),t.add(b.group)),e&&t.css(e),t.attr(b.attribs).animate(d,b.isNew?!1:m,c);else if(t){const f=()=>{a.graphic=t=t&&t.destroy();"function"===typeof c&&c()};Object.keys(d).length?t.animate(d,void 0,()=>f()):f()}}}});
c(a,"Series/Treemap/TreemapPoint.js",[a["Series/DrawPointUtilities.js"],a["Core/Series/SeriesRegistry.js"],a["Core/Utilities.js"]],function(a,d,c){const {series:{prototype:{pointClass:b}},seriesTypes:{pie:{prototype:{pointClass:e}},scatter:{prototype:{pointClass:p}}}}=d,{extend:k,isNumber:m,pick:t}=c;class f extends p{constructor(){super(...arguments);this.series=this.options=this.node=this.name=void 0;this.shapeType="rect";this.value=void 0}draw(f){a.draw(this,f)}getClassName(){let a=b.prototype.getClassName.call(this),
f=this.series,d=f.options;this.node.level<=f.nodeMap[f.rootNode].level?a+=" highcharts-above-level":this.node.isLeaf||t(d.interactByLeaf,!d.allowTraversingTree)?this.node.isLeaf||(a+=" highcharts-internal-node"):a+=" highcharts-internal-node-interactive";return a}isValid(){return!(!this.id&&!m(this.value))}setState(a){b.prototype.setState.call(this,a);this.graphic&&this.graphic.attr({zIndex:"hover"===a?1:0})}shouldDraw(){return m(this.plotY)&&null!==this.y}}k(f.prototype,{setVisible:e.prototype.setVisible});
return f});c(a,"Series/Treemap/TreemapUtilities.js",[a["Core/Utilities.js"]],function(a){const {objectEach:b}=a;var c;(function(a){function d(a,b,c=this){a=b.call(c,a);!1!==a&&d(a,b,c)}a.AXIS_MAX=100;a.isBoolean=function(a){return"boolean"===typeof a};a.eachObject=function(a,d,c){c=c||this;b(a,function(b,f){d.call(c,b,f,a)})};a.recursive=d})(c||(c={}));return c});c(a,"Series/TreeUtilities.js",[a["Core/Color/Color.js"],a["Core/Utilities.js"]],function(a,c){function b(a,c){var f=c.before;const h=c.idRoot,
e=c.mapIdToNode[h],k=c.points[a.i],m=k&&k.options||{},r=[];let x=0;a.levelDynamic=a.level-(!1!==c.levelIsConstant?0:e.level);a.name=t(k&&k.name,"");a.visible=h===a.id||!0===c.visible;"function"===typeof f&&(a=f(a,c));a.children.forEach((f,h)=>{const D=d({},c);d(D,{index:h,siblings:a.children.length,visible:a.visible});f=b(f,D);r.push(f);f.visible&&(x+=f.val)});f=t(m.value,x);a.visible=0<=f&&(0<x||a.visible);a.children=r;a.childrenTotal=x;a.isLeaf=a.visible&&!x;a.val=f;return a}const {extend:d,isArray:r,
isNumber:p,isObject:k,merge:m,pick:t}=c;return{getColor:function(f,b){const c=b.index;var d=b.mapOptionsToLevel;const e=b.parentColor,h=b.parentColorIndex,k=b.series;var m=b.colors;const x=b.siblings;var r=k.points,p=k.chart.options.chart;let D;var u;let I;if(f){r=r[f.i];f=d[f.level]||{};if(d=r&&f.colorByPoint){D=r.index%(m?m.length:p.colorCount);var y=m&&m[D]}if(!k.chart.styledMode){m=r&&r.options.color;p=f&&f.color;if(u=e)u=(u=f&&f.colorVariation)&&"brightness"===u.key&&c&&x?a.parse(e).brighten(c/
x*u.to).get():e;u=t(m,p,y,u,k.color)}I=t(r&&r.options.colorIndex,f&&f.colorIndex,D,h,b.colorIndex)}return{color:u,colorIndex:I}},getLevelOptions:function(a){let b={},c,d,f;if(k(a)){f=p(a.from)?a.from:1;var e=a.levels;d={};c=k(a.defaults)?a.defaults:{};r(e)&&(d=e.reduce((a,b)=>{let d,e;k(b)&&p(b.level)&&(e=m({},b),d=t(e.levelIsConstant,c.levelIsConstant),delete e.levelIsConstant,delete e.level,b=b.level+(d?0:f-1),k(a[b])?m(!0,a[b],e):a[b]=e);return a},{}));e=p(a.to)?a.to:1;for(a=0;a<=e;a++)b[a]=m({},
c,k(d[a])?d[a]:{})}return b},setTreeValues:b,updateRootId:function(a){if(k(a)){var b=k(a.options)?a.options:{};b=t(a.rootNode,b.rootId,"");k(a.userOptions)&&(a.userOptions.rootId=b);a.rootNode=b}return b}}});c(a,"Extensions/Breadcrumbs/BreadcrumbsDefaults.js",[],function(){return{lang:{mainBreadcrumb:"Main"},options:{buttonTheme:{fill:"none",height:18,padding:2,"stroke-width":0,zIndex:7,states:{select:{fill:"none"}},style:{color:"#334eff"}},buttonSpacing:5,floating:!1,format:void 0,relativeTo:"plotBox",
rtl:!1,position:{align:"left",verticalAlign:"top",x:0,y:void 0},separator:{text:"/",style:{color:"#666666",fontSize:"0.8em"}},showFullPath:!0,style:{},useHTML:!1,zIndex:7}}});c(a,"Extensions/Breadcrumbs/Breadcrumbs.js",[a["Extensions/Breadcrumbs/BreadcrumbsDefaults.js"],a["Core/Chart/Chart.js"],a["Core/Templating.js"],a["Core/Utilities.js"]],function(a,c,e,B){function b(){if(this.breadcrumbs){const a=this.resetZoomButton&&this.resetZoomButton.getBBox(),b=this.breadcrumbs.options;a&&"right"===b.position.align&&
"plotBox"===b.relativeTo&&this.breadcrumbs.alignBreadcrumbsGroup(-a.width-b.buttonSpacing)}}function d(){this.breadcrumbs&&(this.breadcrumbs.destroy(),this.breadcrumbs=void 0)}function k(){const a=this.breadcrumbs;if(a&&!a.options.floating&&a.level){var b=a.options,c=b.buttonTheme;c=(c.height||0)+2*(c.padding||0)+b.buttonSpacing;b=b.position.verticalAlign;"bottom"===b?(this.marginBottom=(this.marginBottom||0)+c,a.yOffset=c):"middle"!==b?(this.plotTop+=c,a.yOffset=-c):a.yOffset=void 0}}function m(){this.breadcrumbs&&
this.breadcrumbs.redraw()}function t(a){!0===a.resetSelection&&this.breadcrumbs&&this.breadcrumbs.alignBreadcrumbsGroup()}const {format:f}=e,{addEvent:h,defined:O,extend:P,fireEvent:G,isString:M,merge:H,objectEach:K,pick:x}=B,L=[];class C{static compose(f,u){B.pushUnique(L,f)&&(h(c,"destroy",d),h(c,"afterShowResetZoom",b),h(c,"getMargins",k),h(c,"redraw",m),h(c,"selection",t));B.pushUnique(L,u)&&P(u.lang,a.lang)}constructor(a,b){this.elementList={};this.isDirty=!0;this.level=0;this.list=[];b=H(a.options.drilldown&&
a.options.drilldown.drillUpButton,C.defaultOptions,a.options.navigation&&a.options.navigation.breadcrumbs,b);this.chart=a;this.options=b||{}}updateProperties(a){this.setList(a);this.setLevel();this.isDirty=!0}setList(a){this.list=a}setLevel(){this.level=this.list.length&&this.list.length-1}getLevel(){return this.level}getButtonText(a){const b=this.chart,c=this.options;var d=b.options.lang;const e=x(c.format,c.showFullPath?"{level.name}":"\u2190 {level.name}");d=d&&x(d.drillUpText,d.mainBreadcrumb);
a=c.formatter&&c.formatter(a)||f(e,{level:a.levelOptions},b)||"";(M(a)&&!a.length||"\u2190 "===a)&&O(d)&&(a=c.showFullPath?d:"\u2190 "+d);return a}redraw(){this.isDirty&&this.render();this.group&&this.group.align();this.isDirty=!1}render(){const a=this.chart,b=this.options;!this.group&&b&&(this.group=a.renderer.g("breadcrumbs-group").addClass("highcharts-no-tooltip highcharts-breadcrumbs").attr({zIndex:b.zIndex}).add());b.showFullPath?this.renderFullPathButtons():this.renderSingleButton();this.alignBreadcrumbsGroup()}renderFullPathButtons(){this.destroySingleButton();
this.resetElementListState();this.updateListElements();this.destroyListElements()}renderSingleButton(){const a=this.chart;var b=this.list;const c=this.options.buttonSpacing;this.destroyListElements();const d=this.group?this.group.getBBox().width:c;b=b[b.length-2];!a.drillUpButton&&0<this.level?a.drillUpButton=this.renderButton(b,d,c):a.drillUpButton&&(0<this.level?this.updateSingleButton():this.destroySingleButton())}alignBreadcrumbsGroup(a){if(this.group){var b=this.options;const d=b.buttonTheme,
f=b.position,e="chart"===b.relativeTo||"spacingBox"===b.relativeTo?void 0:"scrollablePlotBox";var c=this.group.getBBox();b=2*(d.padding||0)+b.buttonSpacing;f.width=c.width+b;f.height=c.height+b;c=H(f);a&&(c.x+=a);this.options.rtl&&(c.x+=f.width);c.y=x(c.y,this.yOffset,0);this.group.align(c,!0,e)}}renderButton(a,b,c){const d=this,f=this.chart,e=d.options,k=H(e.buttonTheme);b=f.renderer.button(d.getButtonText(a),b,c,function(b){const c=e.events&&e.events.click;let l;c&&(l=c.call(d,b,a));!1!==l&&(b.newLevel=
e.showFullPath?a.level:d.level-1,G(d,"up",b))},k).addClass("highcharts-breadcrumbs-button").add(d.group);f.styledMode||b.attr(e.style);return b}renderSeparator(a,b){const c=this.chart,d=this.options.separator;a=c.renderer.label(d.text,a,b,void 0,void 0,void 0,!1).addClass("highcharts-breadcrumbs-separator").add(this.group);c.styledMode||a.css(d.style);return a}update(a){H(!0,this.options,a);this.destroy();this.isDirty=!0}updateSingleButton(){const a=this.chart,b=this.list[this.level-1];a.drillUpButton&&
a.drillUpButton.attr({text:this.getButtonText(b)})}destroy(){this.destroySingleButton();this.destroyListElements(!0);this.group&&this.group.destroy();this.group=void 0}destroyListElements(a){const b=this.elementList;K(b,(c,d)=>{if(a||!b[d].updated)c=b[d],c.button&&c.button.destroy(),c.separator&&c.separator.destroy(),delete c.button,delete c.separator,delete b[d]});a&&(this.elementList={})}destroySingleButton(){this.chart.drillUpButton&&(this.chart.drillUpButton.destroy(),this.chart.drillUpButton=
void 0)}resetElementListState(){K(this.elementList,a=>{a.updated=!1})}updateListElements(){const a=this.elementList,b=this.options.buttonSpacing,c=this.list,d=this.options.rtl,f=d?-1:1,e=function(a,b){return f*a.getBBox().width+f*b},k=function(a,b,g){a.translate(b-a.getBBox().width,g)};let h=this.group?e(this.group,b):b,m,l;for(let A=0,E=c.length;A<E;++A){const g=A===E-1;let n,q;l=c[A];a[l.level]?(m=a[l.level],n=m.button,m.separator||g?m.separator&&g&&(m.separator.destroy(),delete m.separator):(h+=
f*b,m.separator=this.renderSeparator(h,b),d&&k(m.separator,h,b),h+=e(m.separator,b)),a[l.level].updated=!0):(n=this.renderButton(l,h,b),d&&k(n,h,b),h+=e(n,b),g||(q=this.renderSeparator(h,b),d&&k(q,h,b),h+=e(q,b)),a[l.level]={button:n,separator:q,updated:!0});n&&n.setState(g?2:0)}}}C.defaultOptions=a.options;"";return C});c(a,"Series/Treemap/TreemapComposition.js",[a["Core/Series/SeriesRegistry.js"],a["Series/Treemap/TreemapUtilities.js"],a["Core/Utilities.js"]],function(a,c,e){({series:a}=a);const {addEvent:b,
extend:d}=e;let p=!1;b(a,"afterBindAxes",function(){let a=this.xAxis,b=this.yAxis,e;a&&b&&(this.is("treemap")?(e={endOnTick:!1,gridLineWidth:0,lineWidth:0,min:0,minPadding:0,max:c.AXIS_MAX,maxPadding:0,startOnTick:!1,title:void 0,tickPositions:[]},d(b.options,e),d(a.options,e),p=!0):p&&(b.setOptions(b.userOptions),a.setOptions(a.userOptions),p=!1))})});c(a,"Series/Treemap/TreemapNode.js",[],function(){class a{constructor(){this.childrenTotal=0;this.visible=!1}init(a,b,c,r,p,k,m){this.id=a;this.i=
b;this.children=c;this.height=r;this.level=p;this.series=k;this.parent=m;return this}}return a});c(a,"Series/Treemap/TreemapSeries.js",[a["Core/Color/Color.js"],a["Series/ColorMapComposition.js"],a["Core/Globals.js"],a["Core/Series/SeriesRegistry.js"],a["Series/Treemap/TreemapAlgorithmGroup.js"],a["Series/Treemap/TreemapPoint.js"],a["Series/Treemap/TreemapUtilities.js"],a["Series/TreeUtilities.js"],a["Extensions/Breadcrumbs/Breadcrumbs.js"],a["Core/Utilities.js"],a["Series/Treemap/TreemapNode.js"]],
function(a,c,e,B,r,p,k,m,t,f,h){const {parse:b}=a;({noop:a}=e);const {series:d,seriesTypes:{column:G,heatmap:M,scatter:H}}=B,{getColor:K,getLevelOptions:x,updateRootId:L}=m,{addEvent:C,correctFloat:D,defined:u,error:I,extend:y,fireEvent:Q,isArray:J,isObject:R,isString:N,merge:w,pick:l,stableSort:A}=f;class E extends H{constructor(){super(...arguments);this.level=this.tree=this.rootNode=this.points=this.options=this.nodeList=this.nodeMap=this.mapOptionsToLevel=this.data=this.axisRatio=void 0}algorithmCalcPoints(a,
b,c,d){let g,n,q,l,z=c.lW,f=c.lH,e=c.plot,k,h=0,m=c.elArr.length-1;b?(z=c.nW,f=c.nH):k=c.elArr[c.elArr.length-1];c.elArr.forEach(function(a){if(b||h<m)0===c.direction?(g=e.x,n=e.y,q=z,l=a/q):(g=e.x,n=e.y,l=f,q=a/l),d.push({x:g,y:n,width:q,height:D(l)}),0===c.direction?e.y+=l:e.x+=q;h+=1});c.reset();0===c.direction?c.width-=z:c.height-=f;e.y=e.parent.y+(e.parent.height-c.height);e.x=e.parent.x+(e.parent.width-c.width);a&&(c.direction=1-c.direction);b||c.addElement(k)}algorithmFill(a,b,c){let g=[],
n,q=b.direction,d=b.x,l=b.y,e=b.width,f=b.height,k,h,m,A;c.forEach(function(c){n=c.val/b.val*b.height*b.width;k=d;h=l;0===q?(A=f,m=n/A,e-=m,d+=m):(m=e,A=n/m,f-=A,l+=A);g.push({x:k,y:h,width:m,height:A});a&&(q=1-q)});return g}algorithmLowAspectRatio(a,b,c){let g=[],n=this,q,d={x:b.x,y:b.y,parent:b},l=0,e=c.length-1,f=new r(b.height,b.width,b.direction,d);c.forEach(function(c){q=c.val/b.val*b.height*b.width;f.addElement(q);f.lP.nR>f.lP.lR&&n.algorithmCalcPoints(a,!1,f,g,d);l===e&&n.algorithmCalcPoints(a,
!0,f,g,d);l+=1});return g}alignDataLabel(a,b,c){const g=c.style;g&&!u(g.textOverflow)&&b.text&&b.getBBox().width>b.text.textWidth&&b.css({textOverflow:"ellipsis",width:g.width+="px"});G.prototype.alignDataLabel.apply(this,arguments);a.dataLabel&&a.dataLabel.attr({zIndex:(a.node.zIndex||0)+1})}calculateChildrenAreas(a,b){let g=this,c=g.options,n=g.mapOptionsToLevel[a.level+1],d=l(g[n&&n.layoutAlgorithm]&&n.layoutAlgorithm,c.layoutAlgorithm),e=c.alternateStartingDirection,f=[];a=a.children.filter(function(a){return!a.ignore});
n&&n.layoutStartingDirection&&(b.direction="vertical"===n.layoutStartingDirection?0:1);f=g[d](b,a);a.forEach(function(a,c){c=f[c];a.values=w(c,{val:a.childrenTotal,direction:e?1-b.direction:b.direction});a.pointValues=w(c,{x:c.x/g.axisRatio,y:k.AXIS_MAX-c.y-c.height,width:c.width/g.axisRatio});a.children.length&&g.calculateChildrenAreas(a,a.values)})}createList(a){var b=this.chart;const c=[];if(b.breadcrumbs){let g=0;c.push({level:g,levelOptions:b.series[0]});b=a.target.nodeMap[a.newRootId];const d=
[];for(;b.parent||""===b.parent;)d.push(b),b=a.target.nodeMap[b.parent];d.reverse().forEach(function(a){c.push({level:++g,levelOptions:a})});1>=c.length&&(c.length=0)}return c}drawDataLabels(){let a=this,b=a.mapOptionsToLevel,c,l;a.points.filter(function(a){return a.node.visible}).forEach(function(g){l=b[g.node.level];c={style:{}};g.node.isLeaf||(c.enabled=!1);l&&l.dataLabels&&(c=w(c,l.dataLabels),a._hasPointLabels=!0);g.shapeArgs&&(c.style.width=g.shapeArgs.width,g.dataLabel&&g.dataLabel.css({width:g.shapeArgs.width+
"px"}));g.dlOptions=w(c,g.options.dataLabels)});d.prototype.drawDataLabels.call(this)}drawPoints(a=this.points){const b=this,c=b.chart,g=c.renderer,d=c.styledMode,l=b.options,f=d?{}:l.shadow,e=l.borderRadius,k=c.pointCount<l.animationLimit,h=l.allowTraversingTree;a.forEach(function(a){const c=a.node.levelDynamic,n={},q={},F={},z="level-group-"+a.node.level,S=!!a.graphic,m=k&&S,T=a.shapeArgs;a.shouldDraw()&&(a.isInside=!0,e&&(q.r=e),w(!0,m?n:q,S?T:{},d?{}:b.pointAttribs(a,a.selected?"select":void 0)),
b.colorAttribs&&d&&y(F,b.colorAttribs(a)),b[z]||(b[z]=g.g(z).attr({zIndex:1E3-(c||0)}).add(b.group),b[z].survive=!0));a.draw({animatableAttribs:n,attribs:q,css:F,group:b[z],renderer:g,shadow:f,shapeArgs:T,shapeType:a.shapeType});h&&a.graphic&&(a.drillId=l.interactByLeaf?b.drillToByLeaf(a):b.drillToByGroup(a))})}drillToByGroup(a){let b=!1;1!==a.node.level-this.nodeMap[this.rootNode].level||a.node.isLeaf||(b=a.id);return b}drillToByLeaf(a){let b=!1;if(a.node.parent!==this.rootNode&&a.node.isLeaf)for(a=
a.node;!b;)a=this.nodeMap[a.parent],a.parent===this.rootNode&&(b=a.id);return b}drillToNode(a,b){I(32,!1,void 0,{"treemap.drillToNode":"use treemap.setRootNode"});this.setRootNode(a,b)}drillUp(){const a=this.nodeMap[this.rootNode];a&&N(a.parent)&&this.setRootNode(a.parent,!0,{trigger:"traverseUpButton"})}getExtremes(){const {dataMin:a,dataMax:b}=d.prototype.getExtremes.call(this,this.colorValueData);this.valueMin=a;this.valueMax=b;return d.prototype.getExtremes.call(this)}getListOfParents(a,b){a=
J(a)?a:[];const c=J(b)?b:[];b=a.reduce(function(a,b,c){b=l(b.parent,"");"undefined"===typeof a[b]&&(a[b]=[]);a[b].push(c);return a},{"":[]});k.eachObject(b,function(a,b,g){""!==b&&-1===c.indexOf(b)&&(a.forEach(function(a){g[""].push(a)}),delete g[b])});return b}getTree(){var a=this.data.map(function(a){return a.id});a=this.getListOfParents(this.data,a);this.nodeMap={};this.nodeList=[];return this.buildTree("",-1,0,a)}buildTree(a,b,c,d,l){let g=this,e=[],f=g.points[b],q=0,n,z;(d[a]||[]).forEach(function(b){z=
g.buildTree(g.points[b].id,b,c+1,d,a);q=Math.max(z.height+1,q);e.push(z)});n=(new g.NodeClass).init(a,b,e,q,c,g,l);e.forEach(a=>{a.parentNode=n});g.nodeMap[n.id]=n;g.nodeList.push(n);f&&(f.node=n,n.point=f);return n}hasData(){return!!this.processedXData.length}init(a,b){const c=this,g=w(b.drillUpButton,b.breadcrumbs);let l;l=C(c,"setOptions",function(a){a=a.userOptions;u(a.allowDrillToNode)&&!u(a.allowTraversingTree)&&(a.allowTraversingTree=a.allowDrillToNode,delete a.allowDrillToNode);u(a.drillUpButton)&&
!u(a.traverseUpButton)&&(a.traverseUpButton=a.drillUpButton,delete a.drillUpButton)});d.prototype.init.call(c,a,b);delete c.opacity;c.eventsToUnbind.push(l);c.options.allowTraversingTree&&(c.eventsToUnbind.push(C(c,"click",c.onClickDrillToNode)),c.eventsToUnbind.push(C(c,"setRootNode",function(a){const b=c.chart;b.breadcrumbs&&b.breadcrumbs.updateProperties(c.createList(a))})),c.eventsToUnbind.push(C(c,"update",function(a,b){(b=this.chart.breadcrumbs)&&a.options.breadcrumbs&&b.update(a.options.breadcrumbs)})),
c.eventsToUnbind.push(C(c,"destroy",function(a){const b=this.chart;b.breadcrumbs&&(b.breadcrumbs.destroy(),a.keepEventsForUpdate||(b.breadcrumbs=void 0))})));a.breadcrumbs||(a.breadcrumbs=new t(a,g));c.eventsToUnbind.push(C(a.breadcrumbs,"up",function(a){a=this.level-a.newLevel;for(let b=0;b<a;b++)c.drillUp()}))}onClickDrillToNode(a){const b=(a=a.point)&&a.drillId;N(b)&&(a.setState(""),this.setRootNode(b,!0,{trigger:"click"}))}pointAttribs(a,c){var g=R(this.mapOptionsToLevel)?this.mapOptionsToLevel:
{};let d=a&&g[a.node.level]||{};g=this.options;let e=c&&g.states&&g.states[c]||{},f=a&&a.getClassName()||"";a={stroke:a&&a.borderColor||d.borderColor||e.borderColor||g.borderColor,"stroke-width":l(a&&a.borderWidth,d.borderWidth,e.borderWidth,g.borderWidth),dashstyle:a&&a.borderDashStyle||d.borderDashStyle||e.borderDashStyle||g.borderDashStyle,fill:a&&a.color||this.color};-1!==f.indexOf("highcharts-above-level")?(a.fill="none",a["stroke-width"]=0):-1!==f.indexOf("highcharts-internal-node-interactive")?
(c=l(e.opacity,g.opacity),a.fill=b(a.fill).setOpacity(c).get(),a.cursor="pointer"):-1!==f.indexOf("highcharts-internal-node")?a.fill="none":c&&(a.fill=b(a.fill).brighten(e.brightness).get());return a}setColorRecursive(a,b,c,d,l){let g=this;var e=g&&g.chart;e=e&&e.options&&e.options.colors;let f;if(a){f=K(a,{colors:e,index:d,mapOptionsToLevel:g.mapOptionsToLevel,parentColor:b,parentColorIndex:c,series:g,siblings:l});if(b=g.points[a.i])b.color=f.color,b.colorIndex=f.colorIndex;(a.children||[]).forEach(function(b,
c){g.setColorRecursive(b,f.color,f.colorIndex,c,a.children.length)})}}setPointValues(){const a=this,{points:b,xAxis:c,yAxis:d}=a,l=a.chart.styledMode;b.forEach(function(b){const {pointValues:g,visible:e}=b.node;if(g&&e){const {height:e,width:q,x:k,y:h}=g;var f=l?0:(a.pointAttribs(b)["stroke-width"]||0)%2/2,n=Math.round(c.toPixels(k,!0))-f;const z=Math.round(c.toPixels(k+q,!0))-f,m=Math.round(d.toPixels(h,!0))-f;f=Math.round(d.toPixels(h+e,!0))-f;n={x:Math.min(n,z),y:Math.min(m,f),width:Math.abs(z-
n),height:Math.abs(f-m)};b.plotX=n.x+n.width/2;b.plotY=n.y+n.height/2;b.shapeArgs=n}else delete b.plotX,delete b.plotY})}setRootNode(a,b,c){a=y({newRootId:a,previousRootId:this.rootNode,redraw:l(b,!0),series:this},c);Q(this,"setRootNode",a,function(a){const b=a.series;b.idPreviousRoot=a.previousRootId;b.rootNode=a.newRootId;b.isDirty=!0;a.redraw&&b.chart.redraw()})}setState(a){this.options.inactiveOtherPoints=!0;d.prototype.setState.call(this,a,!1);this.options.inactiveOtherPoints=!1}setTreeValues(a){let b=
this;var c=b.options;let g=b.nodeMap[b.rootNode];c=k.isBoolean(c.levelIsConstant)?c.levelIsConstant:!0;let d=0,f=[],e,h=b.points[a.i];a.children.forEach(function(a){a=b.setTreeValues(a);f.push(a);a.ignore||(d+=a.val)});A(f,function(a,b){return(a.sortIndex||0)-(b.sortIndex||0)});e=l(h&&h.options.value,d);h&&(h.value=e);y(a,{children:f,childrenTotal:d,ignore:!(l(h&&h.visible,!0)&&0<e),isLeaf:a.visible&&!d,levelDynamic:a.level-(c?0:g.level),name:l(h&&h.name,""),sortIndex:l(h&&h.sortIndex,-e),val:e});
return a}sliceAndDice(a,b){return this.algorithmFill(!0,a,b)}squarified(a,b){return this.algorithmLowAspectRatio(!0,a,b)}strip(a,b){return this.algorithmLowAspectRatio(!1,a,b)}stripes(a,b){return this.algorithmFill(!1,a,b)}translate(){let a=this;var b=a.options,c=L(a);let e,f;d.prototype.translate.call(a);f=a.tree=a.getTree();e=a.nodeMap[c];""===c||e&&e.children.length||(a.setRootNode("",!1),c=a.rootNode,e=a.nodeMap[c]);a.mapOptionsToLevel=x({from:e.level+1,levels:b.levels,to:f.height,defaults:{levelIsConstant:a.options.levelIsConstant,
colorByPoint:b.colorByPoint}});k.recursive(a.nodeMap[a.rootNode],function(b){let c=!1,d=b.parent;b.visible=!0;if(d||""===d)c=a.nodeMap[d];return c});k.recursive(a.nodeMap[a.rootNode].children,function(a){let b=!1;a.forEach(function(a){a.visible=!0;a.children.length&&(b=(b||[]).concat(a.children))});return b});a.setTreeValues(f);a.axisRatio=a.xAxis.len/a.yAxis.len;a.nodeMap[""].pointValues=c={x:0,y:0,width:k.AXIS_MAX,height:k.AXIS_MAX};a.nodeMap[""].values=c=w(c,{width:c.width*a.axisRatio,direction:"vertical"===
b.layoutStartingDirection?0:1,val:f.val});a.calculateChildrenAreas(f,c);a.colorAxis||b.colorByPoint||a.setColorRecursive(a.tree);b.allowTraversingTree&&(b=e.pointValues,a.xAxis.setExtremes(b.x,b.x+b.width,!1),a.yAxis.setExtremes(b.y,b.y+b.height,!1),a.xAxis.setScale(),a.yAxis.setScale());a.setPointValues()}}E.defaultOptions=w(H.defaultOptions,{allowTraversingTree:!1,animationLimit:250,borderRadius:0,showInLegend:!1,marker:void 0,colorByPoint:!1,dataLabels:{defer:!1,enabled:!0,formatter:function(){const a=
this&&this.point?this.point:{};return N(a.name)?a.name:""},inside:!0,verticalAlign:"middle"},tooltip:{headerFormat:"",pointFormat:"<b>{point.name}</b>: {point.value}<br/>"},ignoreHiddenPoint:!0,layoutAlgorithm:"sliceAndDice",layoutStartingDirection:"vertical",alternateStartingDirection:!1,levelIsConstant:!0,traverseUpButton:{position:{align:"right",x:-10,y:10}},borderColor:"#e6e6e6",borderWidth:1,colorKey:"colorValue",opacity:.15,states:{hover:{borderColor:"#999999",brightness:M?0:.1,halo:!1,opacity:.75,
shadow:!1}},legendSymbol:"rectangle"});y(E.prototype,{buildKDTree:a,colorAttribs:c.seriesMembers.colorAttribs,colorKey:"colorValue",directTouch:!0,getExtremesFromAll:!0,getSymbol:a,optionalAxis:"colorAxis",parallelArrays:["x","y","value","colorValue"],pointArrayMap:["value"],pointClass:p,NodeClass:h,trackerGroups:["group","dataLabelsGroup"],utils:{recursive:k.recursive}});c.compose(E);B.registerSeriesType("treemap",E);"";return E});c(a,"Series/Sunburst/SunburstPoint.js",[a["Core/Series/SeriesRegistry.js"],
a["Core/Utilities.js"]],function(a,c){const {series:{prototype:{pointClass:b}},seriesTypes:{treemap:{prototype:{pointClass:d}}}}=a,{correctFloat:r,extend:p}=c;class k extends d{constructor(){super(...arguments);this.shapeType=this.shapeExisting=this.series=this.options=this.node=void 0}getDataLabelPath(a){let b=this.series.chart.renderer,c=this.shapeExisting,d=c.start,e=c.end;var k=d+(e-d)/2;k=0>k&&k>-Math.PI||k>Math.PI;a=c.r+(a.options.distance||0);let m;d===-Math.PI/2&&r(e)===r(1.5*Math.PI)&&(d=
-Math.PI+Math.PI/360,e=-Math.PI/360,k=!0);e-d>Math.PI&&(k=!1,m=!0,e-d>2*Math.PI-.01&&(d+=.01,e-=.01));this.dataLabelPath&&(this.dataLabelPath=this.dataLabelPath.destroy());return this.dataLabelPath=b.arc({open:!0,longArc:m?1:0}).attr({start:k?d:e,end:k?e:d,clockwise:+k,x:c.x,y:c.y,r:(a+c.innerR)/2}).add(b.defs)}isValid(){return!0}}p(k.prototype,{getClassName:b.prototype.getClassName,haloPath:b.prototype.haloPath,setState:b.prototype.setState});return k});c(a,"Series/Sunburst/SunburstUtilities.js",
[a["Core/Series/SeriesRegistry.js"],a["Core/Utilities.js"]],function(a,c){const {seriesTypes:{treemap:b}}=a,{isNumber:d,isObject:r,merge:p}=c;var k;(function(a){function c(a,b){let c=[];if(d(a)&&d(b)&&a<=b)for(;a<=b;a++)c.push(a);return c}a.recursive=b.prototype.utils.recursive;a.calculateLevelSizes=function(a,b){let e;b=r(b)?b:{};let f=0,k,m,h,t;r(a)&&(e=p({},a),a=d(b.from)?b.from:0,t=d(b.to)?b.to:0,m=c(a,t),a=Object.keys(e).filter(function(a){return-1===m.indexOf(+a)}),k=h=d(b.diffRadius)?b.diffRadius:
0,m.forEach(function(a){a=e[a];const b=a.levelSize.unit,c=a.levelSize.value;"weight"===b?f+=c:"percentage"===b?(a.levelSize={unit:"pixels",value:c/100*k},h-=a.levelSize.value):"pixels"===b&&(h-=c)}),m.forEach(function(a){var b=e[a];"weight"===b.levelSize.unit&&(b=b.levelSize.value,e[a].levelSize={unit:"pixels",value:b/f*h})}),a.forEach(function(a){e[a].levelSize={value:0,unit:"pixels"}}));return e};a.getLevelFromAndTo=function({level:a,height:b}){return{from:0<a?a:1,to:a+b}};a.range=c})(k||(k={}));
return k});c(a,"Series/Sunburst/SunburstNode.js",[a["Series/Treemap/TreemapNode.js"]],function(a){class b extends a{}return b});c(a,"Series/Sunburst/SunburstSeries.js",[a["Series/CenteredUtilities.js"],a["Core/Globals.js"],a["Core/Series/SeriesRegistry.js"],a["Series/Sunburst/SunburstPoint.js"],a["Series/Sunburst/SunburstUtilities.js"],a["Series/TreeUtilities.js"],a["Core/Utilities.js"],a["Series/Sunburst/SunburstNode.js"]],function(a,c,e,B,r,p,k,m){function b(a,b){var c=b.mapIdToNode,d=a.parent;
d=d?c[d]:void 0;const e=b.series,f=e.chart;c=e.points[a.i];d=M(a,{colors:e.options.colors||f&&f.options.colors,colorIndex:e.colorIndex,index:b.index,mapOptionsToLevel:b.mapOptionsToLevel,parentColor:d&&d.color,parentColorIndex:d&&d.colorIndex,series:b.series,siblings:b.siblings});a.color=d.color;a.colorIndex=d.colorIndex;c&&(c.color=a.color,c.colorIndex=a.colorIndex,a.sliced=a.id!==b.idRoot?c.sliced:!1);return a}const {getCenter:d,getStartAndEndRadians:h}=a;({noop:a}=c);const {series:O,seriesTypes:{column:P,
treemap:G}}=e,{getColor:M,getLevelOptions:H,setTreeValues:K,updateRootId:x}=p,{defined:L,error:C,extend:D,fireEvent:u,isNumber:I,isObject:y,isString:Q,merge:J,splat:R}=k,N=180/Math.PI;class w extends G{constructor(){super(...arguments);this.tree=this.startAndEndRadians=this.shapeRoot=this.points=this.options=this.nodeMap=this.mapOptionsToLevel=this.data=this.center=void 0}alignDataLabel(a,b,c){if(!c.textPath||!c.textPath.enabled)return super.alignDataLabel.apply(this,arguments)}animate(a){var b=this.chart;
let c=[b.plotWidth/2,b.plotHeight/2],d=b.plotLeft,e=b.plotTop;b=this.group;a?(a={translateX:c[0]+d,translateY:c[1]+e,scaleX:.001,scaleY:.001,rotation:10,opacity:.01},b.attr(a)):(a={translateX:d,translateY:e,scaleX:1,scaleY:1,rotation:0,opacity:1},b.animate(a,this.options.animation))}drawPoints(){let a=this,b=a.mapOptionsToLevel,c=a.shapeRoot,d=a.group,e=a.hasRendered,f=a.rootNode,k=a.idPreviousRoot,m=a.nodeMap;var h=m[k];let r=h&&h.shapeArgs;h=a.points;let p=a.startAndEndRadians,t=a.chart;var u=t&&
t.options&&t.options.chart||{};let x="boolean"===typeof u.animation?u.animation:!0,w=a.center[3]/2,B=a.chart.renderer,C,H=!1,G=!1;if(u=!!(x&&e&&f!==k&&a.dataLabelsGroup))a.dataLabelsGroup.attr({opacity:0}),C=function(){H=!0;a.dataLabelsGroup&&a.dataLabelsGroup.animate({opacity:1,visibility:"inherit"})};h.forEach(function(g){var l=g.node,h=b[l.level];var n=g.shapeExisting||{};let q=l.shapeArgs||{},z,A=!(!l.visible||!l.shapeArgs);q.borderRadius=a.options.borderRadius;if(e&&x){var E={};var u={end:q.end,
start:q.start,innerR:q.innerR,r:q.r,x:q.x,y:q.y};A?!g.graphic&&r&&(E=f===g.id?{start:p.start,end:p.end}:r.end<=q.start?{start:p.end,end:p.end}:{start:p.start,end:p.start},E.innerR=E.r=w):g.graphic&&(k===g.id?u={innerR:w,r:w}:c&&(u=c.end<=n.start?{innerR:w,r:w,start:p.end,end:p.end}:{innerR:w,r:w,start:p.start,end:p.start}));n=E}else u=q,n={};E=[q.plotX,q.plotY];if(!g.node.isLeaf)if(f===g.id){var v=m[f];v=v.parent}else v=g.id;D(g,{shapeExisting:q,tooltipPos:E,drillId:v,name:""+(g.name||g.id||g.index),
plotX:q.plotX,plotY:q.plotY,value:l.val,isInside:A,isNull:!A});v=g.options;l=y(q)?q:{};v=y(v)?v.dataLabels:{};h=R(y(h)?h.dataLabels:{})[0];h=J({style:{}},h,v);v=h.rotationMode;if(!I(h.rotation)){if("auto"===v||"circular"===v)if(h.useHTML&&"circular"===v&&(v="auto"),1>g.innerArcLength&&g.outerArcLength>l.radius){var F=0;g.dataLabelPath&&"circular"===v&&(h.textPath={enabled:!0})}else 1<g.innerArcLength&&g.outerArcLength>1.5*l.radius?"circular"===v?h.textPath={enabled:!0,attributes:{dy:5}}:v="parallel":
(g.dataLabel&&g.dataLabel.textPath&&"circular"===v&&(h.textPath={enabled:!1}),v="perpendicular");"auto"!==v&&"circular"!==v&&(g.dataLabel&&g.dataLabel.textPath&&(h.textPath={enabled:!1}),F=l.end-(l.end-l.start)/2);"parallel"===v?h.style.width=Math.min(2.5*l.radius,(g.outerArcLength+g.innerArcLength)/2):!L(h.style.width)&&l.radius&&(h.style.width=1===g.node.level?2*l.radius:l.radius);"perpendicular"===v&&16>g.outerArcLength&&(h.style.width=1);h.style.width=Math.max(h.style.width-2*(h.padding||0),1);
F=F*N%180;"parallel"===v&&(F-=90);90<F?F-=180:-90>F&&(F+=180);h.rotation=F}h.textPath&&(0===g.shapeExisting.innerR&&h.textPath.enabled?(h.rotation=0,h.textPath.enabled=!1,h.style.width=Math.max(2*g.shapeExisting.r-2*(h.padding||0),1)):g.dlOptions&&g.dlOptions.textPath&&!g.dlOptions.textPath.enabled&&"circular"===v&&(h.textPath.enabled=!0),h.textPath.enabled&&(h.rotation=0,h.style.width=Math.max((g.outerArcLength+g.innerArcLength)/2-2*(h.padding||0),1)));0===h.rotation&&(h.rotation=.001);F=h;g.dlOptions=
F;!G&&A&&(G=!0,z=C);g.draw({animatableAttribs:u,attribs:D(n,!t.styledMode&&a.pointAttribs(g,g.selected&&"select")),onComplete:z,group:d,renderer:B,shapeType:"arc",shapeArgs:q})});u&&G?(a.hasRendered=!1,a.options.dataLabels.defer=!0,O.prototype.drawDataLabels.call(a),a.hasRendered=!0,H&&C()):O.prototype.drawDataLabels.call(a);a.idPreviousRoot=f}layoutAlgorithm(a,b,c){let d=a.start,e=a.end-d,f=a.val,h=a.x,l=a.y,k=c&&y(c.levelSize)&&I(c.levelSize.value)?c.levelSize.value:0,m=a.r,r=m+k,p=c&&I(c.slicedOffset)?
c.slicedOffset:0;return(b||[]).reduce(function(a,b){const c=1/f*b.val*e;var g=d+c/2,q=h+Math.cos(g)*p;g=l+Math.sin(g)*p;b={x:b.sliced?q:h,y:b.sliced?g:l,innerR:m,r,radius:k,start:d,end:d+c};a.push(b);d=b.end;return a},[])}setRootNode(a,b,c){if(1===this.nodeMap[a].level&&1===this.nodeList.filter(a=>1===a.level).length){if(""===this.idPreviousRoot)return;a=""}super.setRootNode(a,b,c)}setShapeArgs(a,b,c){let d=[],e=c[a.level+1];a=a.children.filter(function(a){return a.visible});d=this.layoutAlgorithm(b,
a,e);a.forEach(function(a,b){b=d[b];const e=b.start+(b.end-b.start)/2;var f=b.innerR+(b.r-b.innerR)/2;const g=b.end-b.start;f=0===b.innerR&&6.28<g?{x:b.x,y:b.y}:{x:b.x+Math.cos(e)*f,y:b.y+Math.sin(e)*f};const h=a.val?a.childrenTotal>a.val?a.childrenTotal:a.val:a.childrenTotal;this.points[a.i]&&(this.points[a.i].innerArcLength=g*b.innerR,this.points[a.i].outerArcLength=g*b.r);a.shapeArgs=J(b,{plotX:f.x,plotY:f.y+4*Math.abs(Math.cos(e))});a.values=J(b,{val:h});a.children.length&&this.setShapeArgs(a,
a.values,c)},this)}translate(){let a=this;var c=a.options;let d=a.center=a.getCenter(),e=a.startAndEndRadians=h(c.startAngle,c.endAngle),f=d[3]/2,k=d[2]/2-f,m=x(a),p=a.nodeMap;let t=p&&p[m],w,B,D={};a.shapeRoot=t&&t.shapeArgs;this.processedXData||this.processData();this.generatePoints();u(this,"afterTranslate");B=a.tree=a.getTree();p=a.nodeMap;t=p[m];var y=Q(t.parent)?t.parent:"";w=p[y];const {from:G,to:I}=r.getLevelFromAndTo(t);y=H({from:G,levels:a.options.levels,to:I,defaults:{colorByPoint:c.colorByPoint,
dataLabels:c.dataLabels,levelIsConstant:c.levelIsConstant,levelSize:c.levelSize,slicedOffset:c.slicedOffset}});y=r.calculateLevelSizes(y,{diffRadius:k,from:G,to:I});K(B,{before:b,idRoot:m,levelIsConstant:c.levelIsConstant,mapOptionsToLevel:y,mapIdToNode:p,points:a.points,series:a});c=p[""].shapeArgs={end:e.end,r:f,start:e.start,val:t.val,x:d[0],y:d[1]};this.setShapeArgs(w,c,y);a.mapOptionsToLevel=y;a.data.forEach(function(b){D[b.id]&&C(31,!1,a.chart);D[b.id]=!0});D={}}}w.defaultOptions=J(G.defaultOptions,
{center:["50%","50%"],clip:!1,colorByPoint:!1,opacity:1,dataLabels:{allowOverlap:!0,defer:!0,rotationMode:"circular",style:{textOverflow:"ellipsis"}},rootId:void 0,levelIsConstant:!0,levelSize:{value:1,unit:"weight"},slicedOffset:10});D(w.prototype,{axisTypes:[],drawDataLabels:a,getCenter:d,isCartesian:!1,onPointSupported:!0,pointAttribs:P.prototype.pointAttribs,pointClass:B,NodeClass:m,utils:r});e.registerSeriesType("sunburst",w);"";return w});c(a,"masters/modules/sunburst.src.js",[a["Core/Globals.js"],
a["Extensions/Breadcrumbs/Breadcrumbs.js"]],function(a,c){a.Breadcrumbs=c;c.compose(a.Chart,a.defaultOptions)})});
//# sourceMappingURL=sunburst.js.map