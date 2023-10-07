/*
 Highcharts Gantt JS v11.1.0 (2023-06-05)

 Tree Grid

 (c) 2016-2021 Jon Arild Nygard

 License: www.highcharts.com/license
*/
'use strict';(function(g){"object"===typeof module&&module.exports?(g["default"]=g,module.exports=g):"function"===typeof define&&define.amd?define("highcharts/modules/treegrid",["highcharts"],function(z){g(z);g.Highcharts=z;return g}):g("undefined"!==typeof Highcharts?Highcharts:void 0)})(function(g){function z(g,v,t,L){g.hasOwnProperty(v)||(g[v]=L.apply(null,t),"function"===typeof CustomEvent&&window.dispatchEvent(new CustomEvent("HighchartsModuleLoaded",{detail:{path:v,module:g[v]}})))}g=g?g._modules:
{};z(g,"Core/Axis/BrokenAxis.js",[g["Core/Axis/Stacking/StackItem.js"],g["Core/Utilities.js"]],function(g,v){const {addEvent:t,find:L,fireEvent:F,isArray:B,isNumber:n,pick:u}=v;var x;(function(a){function y(){"undefined"!==typeof this.brokenAxis&&this.brokenAxis.setBreaks(this.options.breaks,!1)}function G(){this.brokenAxis&&this.brokenAxis.hasBreaks&&(this.options.ordinal=!1)}function r(){const k=this.brokenAxis;if(k&&k.hasBreaks){const b=this.tickPositions,a=this.tickPositions.info,d=[];for(let a=
0;a<b.length;a++)k.isInAnyBreak(b[a])||d.push(b[a]);this.tickPositions=d;this.tickPositions.info=a}}function c(){this.brokenAxis||(this.brokenAxis=new E(this))}function I(){const {isDirty:k,options:{connectNulls:b},points:a,xAxis:d,yAxis:c}=this;if(k){let e=a.length;for(;e--;){const k=a[e],D=!(null===k.y&&!1===b)&&(d&&d.brokenAxis&&d.brokenAxis.isInAnyBreak(k.x,!0)||c&&c.brokenAxis&&c.brokenAxis.isInAnyBreak(k.y,!0));k.visible=D?!1:!1!==k.options.visible}}}function q(){this.drawBreaks(this.xAxis,
["x"]);this.drawBreaks(this.yAxis,u(this.pointArrayMap,["y"]))}function f(k,a){const b=this,d=b.points;let c,e,m,w;if(k&&k.brokenAxis&&k.brokenAxis.hasBreaks){const D=k.brokenAxis;a.forEach(function(a){c=D&&D.breakArray||[];e=k.isXAxis?k.min:u(b.options.threshold,k.min);d.forEach(function(d){w=u(d["stack"+a.toUpperCase()],d[a]);c.forEach(function(a){if(n(e)&&n(w)){m=!1;if(e<a.from&&w>a.to||e>a.from&&w<a.from)m="pointBreak";else if(e<a.from&&w>a.from&&w<a.to||e>a.from&&w>a.to&&w<a.from)m="pointInBreak";
m&&F(k,m,{point:d,brk:a})}})})})}}function l(){var a=this.currentDataGrouping,b=a&&a.gapSize;a=this.points.slice();const c=this.yAxis;let d=this.options.gapSize,f=a.length-1;var e;if(d&&0<f)for("value"!==this.options.gapUnit&&(d*=this.basePointRange),b&&b>d&&b>=this.basePointRange&&(d=b);f--;)e&&!1!==e.visible||(e=a[f+1]),b=a[f],!1!==e.visible&&!1!==b.visible&&(e.x-b.x>d&&(e=(b.x+e.x)/2,a.splice(f+1,0,{isNull:!0,x:e}),c.stacking&&this.options.stacking&&(e=c.stacking.stacks[this.stackKey][e]=new g(c,
c.options.stackLabels,!1,e,this.stack),e.total=0)),e=b);return this.getGraphPath(a)}const p=[];a.compose=function(a,b){v.pushUnique(p,a)&&(a.keepProps.push("brokenAxis"),t(a,"init",c),t(a,"afterInit",y),t(a,"afterSetTickPositions",r),t(a,"afterSetOptions",G));if(v.pushUnique(p,b)){const a=b.prototype;a.drawBreaks=f;a.gappedPath=l;t(b,"afterGeneratePoints",I);t(b,"afterRender",q)}return a};class E{static isInBreak(a,b){const c=a.repeat||Infinity,d=a.from,k=a.to-a.from;b=b>=d?(b-d)%c:c-(d-b)%c;return a.inclusive?
b<=k:b<k&&0!==b}static lin2Val(a){var b=this.brokenAxis;b=b&&b.breakArray;if(!b||!n(a))return a;let c,d;for(d=0;d<b.length&&!(c=b[d],c.from>=a);d++)c.to<a?a+=c.len:E.isInBreak(c,a)&&(a+=c.len);return a}static val2Lin(a){var b=this.brokenAxis;b=b&&b.breakArray;if(!b||!n(a))return a;let c=a,d,f;for(f=0;f<b.length;f++)if(d=b[f],d.to<=a)c-=d.len;else if(d.from>=a)break;else if(E.isInBreak(d,a)){c-=a-d.from;break}return c}constructor(a){this.hasBreaks=!1;this.axis=a}findBreakAt(a,b){return L(b,function(b){return b.from<
a&&a<b.to})}isInAnyBreak(a,b){const c=this.axis,d=c.options.breaks||[];let f=d.length,e,m,w;if(f&&n(a)){for(;f--;)E.isInBreak(d[f],a)&&(e=!0,m||(m=u(d[f].showPoints,!c.isXAxis)));w=e&&b?e&&!m:e}return w}setBreaks(a,b){const c=this,d=c.axis,f=B(a)&&!!a.length;d.isDirty=c.hasBreaks!==f;c.hasBreaks=f;a!==d.options.breaks&&(d.options.breaks=d.userOptions.breaks=a);d.forceRedraw=!0;d.series.forEach(function(a){a.isDirty=!0});f||d.val2lin!==E.val2Lin||(delete d.val2lin,delete d.lin2val);f&&(d.userOptions.ordinal=
!1,d.lin2val=E.lin2Val,d.val2lin=E.val2Lin,d.setExtremes=function(a,b,f,l,C){if(c.hasBreaks){const d=this.options.breaks||[];let e;for(;e=c.findBreakAt(a,d);)a=e.to;for(;e=c.findBreakAt(b,d);)b=e.from;b<a&&(b=a)}d.constructor.prototype.setExtremes.call(this,a,b,f,l,C)},d.setAxisTranslation=function(){d.constructor.prototype.setAxisTranslation.call(this);c.unitLength=void 0;if(c.hasBreaks){const a=d.options.breaks||[],b=[],f=[],l=u(d.pointRangePadding,0);let C=0,r,p,k=d.userMin||d.min,q=d.userMax||
d.max,h,A;a.forEach(function(h){p=h.repeat||Infinity;n(k)&&n(q)&&(E.isInBreak(h,k)&&(k+=h.to%p-k%p),E.isInBreak(h,q)&&(q-=q%p-h.from%p))});a.forEach(function(a){h=a.from;p=a.repeat||Infinity;if(n(k)&&n(q)){for(;h-p>k;)h-=p;for(;h<k;)h+=p;for(A=h;A<q;A+=p)b.push({value:A,move:"in"}),b.push({value:A+a.to-a.from,move:"out",size:a.breakSize})}});b.sort(function(h,a){return h.value===a.value?("in"===h.move?0:1)-("in"===a.move?0:1):h.value-a.value});r=0;h=k;b.forEach(function(a){r+="in"===a.move?1:-1;1===
r&&"in"===a.move&&(h=a.value);0===r&&n(h)&&(f.push({from:h,to:a.value,len:a.value-h-(a.size||0)}),C+=a.value-h-(a.size||0))});c.breakArray=f;n(k)&&n(q)&&n(d.min)&&(c.unitLength=q-k-C+l,F(d,"afterBreaks"),d.staticScale?d.transA=d.staticScale:c.unitLength&&(d.transA*=(q-d.min+l)/c.unitLength),l&&(d.minPixelPadding=d.transA*(d.minPointOffset||0)),d.min=k,d.max=q)}});u(b,!0)&&d.chart.redraw()}}a.Additions=E})(x||(x={}));return x});z(g,"Core/Axis/GridAxis.js",[g["Core/Axis/Axis.js"],g["Core/Globals.js"],
g["Core/Utilities.js"]],function(g,v,t){function F(a,A){const h={width:0,height:0};A.forEach(function(A){A=a[A];let c,b;t.isObject(A,!0)&&(b=t.isObject(A.label,!0)?A.label:{},A=b.getBBox?b.getBBox().height:0,b.textStr&&!m(b.textPxLength)&&(b.textPxLength=b.getBBox().width),c=m(b.textPxLength)?Math.round(b.textPxLength):0,b.textStr&&(c=Math.round(b.getBBox().width)),h.height=Math.max(A,h.height),h.width=Math.max(c,h.width))});"treegrid"===this.options.type&&this.treeGrid&&this.treeGrid.mapOfPosToGridNode&&
(h.width+=this.options.labels.indentation*((this.treeGrid.mapOfPosToGridNode[-1].height||0)-1));return h}function z(){const {grid:a}=this;(a&&a.columns||[]).forEach(function(a){a.getOffset()})}function B(a){if(!0===(this.options.grid||{}).enabled){const {axisTitle:b,height:A,horiz:c,left:d,offset:e,opposite:f,options:m,top:C,width:l}=this;var h=this.tickSize();const p=b&&b.getBBox().width,k=m.title.x,w=m.title.y,q=K(m.title.margin,c?5:10),r=b?this.chart.renderer.fontMetrics(b).f:0;h=(c?C+A:d)+(c?
1:-1)*(f?-1:1)*(h?h[0]/2:0)+(this.side===H.bottom?r:0);a.titlePosition.x=c?d-(p||0)/2-q+k:h+(f?l:0)+e+k;a.titlePosition.y=c?h-(f?A:0)+(f?r:-r)/2+e+w:C-q+w}}function n(){const {chart:a,options:{grid:b={}},userOptions:c}=this;if(b.enabled){var e=this.options;e.labels.align=K(e.labels.align,"center");this.categories||(e.showLastLabel=!1);this.labelRotation=0;e.labels.rotation=0}if(b.columns){e=this.grid.columns=[];let h=this.grid.columnIndex=0;for(;++h<b.columns.length;){var f=w(c,b.columns[b.columns.length-
h-1],{isInternal:!0,linkedTo:0,type:"category",scrollbar:{enabled:!1}});delete f.grid.columns;f=new g(this.chart,f,"yAxis");f.grid.isColumn=!0;f.grid.columnIndex=h;d(a.axes,f);d(a[this.coll]||[],f);e.push(f)}}}function u(){var a=this.grid,b=this.options;if(!0===(b.grid||{}).enabled){var c=this.min||0;const h=this.max||0;this.maxLabelDimensions=this.getMaxLabelDimensions(this.ticks,this.tickPositions);this.rightWall&&this.rightWall.destroy();if(this.grid&&this.grid.isOuterAxis()&&this.axisLine){var d=
b.lineWidth;if(d){d=this.getLinePath(d);var e=d[0],f=d[1],m=((this.tickSize("tick")||[1])[0]-1)*(this.side===H.top||this.side===H.left?-1:1);"M"===e[0]&&"L"===f[0]&&(this.horiz?(e[2]+=m,f[2]+=m):(e[1]+=m,f[1]+=m));!this.horiz&&this.chart.marginRight&&(e=[e,["L",this.left,e[2]||0]],m=["L",this.chart.chartWidth-this.chart.marginRight,this.toPixels(h+this.tickmarkOffset)],f=[["M",f[1]||0,this.toPixels(h+this.tickmarkOffset)],m],this.grid.upperBorder||0===c%1||(this.grid.upperBorder=this.grid.renderBorder(e)),
this.grid.upperBorder&&(this.grid.upperBorder.attr({stroke:b.lineColor,"stroke-width":b.lineWidth}),this.grid.upperBorder.animate({d:e})),this.grid.lowerBorder||0===h%1||(this.grid.lowerBorder=this.grid.renderBorder(f)),this.grid.lowerBorder&&(this.grid.lowerBorder.attr({stroke:b.lineColor,"stroke-width":b.lineWidth}),this.grid.lowerBorder.animate({d:f})));this.grid.axisLineExtra?(this.grid.axisLineExtra.attr({stroke:b.lineColor,"stroke-width":b.lineWidth}),this.grid.axisLineExtra.animate({d})):this.grid.axisLineExtra=
this.grid.renderBorder(d);this.axisLine[this.showAxis?"show":"hide"]()}}(a&&a.columns||[]).forEach(a=>a.render());if(!this.horiz&&this.chart.hasRendered&&(this.scrollbar||this.linkedParent&&this.linkedParent.scrollbar)){a=this.tickmarkOffset;b=this.tickPositions[this.tickPositions.length-1];d=this.tickPositions[0];let e,f;for(;(e=this.hiddenLabels.pop())&&e.element;)e.show();for(;(f=this.hiddenMarks.pop())&&f.element;)f.show();(e=this.ticks[d].label)&&(c-d>a?this.hiddenLabels.push(e.hide()):e.show());
(e=this.ticks[b].label)&&(b-h>a?this.hiddenLabels.push(e.hide()):e.show());(c=this.ticks[b].mark)&&b-h<a&&0<b-h&&this.ticks[b].isLast&&this.hiddenMarks.push(c.hide())}}}function x(){const a=this.tickPositions&&this.tickPositions.info,b=this.options,c=this.userOptions.labels||{};(b.grid||{}).enabled&&(this.horiz?(this.series.forEach(a=>{a.options.pointRange=0}),a&&b.dateTimeLabelFormats&&b.labels&&!D(c.align)&&(!1===b.dateTimeLabelFormats[a.unitName].range||1<a.count)&&(b.labels.align="left",D(c.x)||
(b.labels.x=3))):"treegrid"!==this.options.type&&this.grid&&this.grid.columns&&(this.minPointOffset=this.tickInterval))}function a(a){const h=this.options;a=a.userOptions;const b=h&&t.isObject(h.grid,!0)?h.grid:{};let c;!0===b.enabled&&(c=w(!0,{className:"highcharts-grid-axis "+(a.className||""),dateTimeLabelFormats:{hour:{list:["%H:%M","%H"]},day:{list:["%A, %e. %B","%a, %e. %b","%E"]},week:{list:["Week %W","W%W"]},month:{list:["%B","%b","%o"]}},grid:{borderWidth:1},labels:{padding:2,style:{fontSize:"0.9em"}},
margin:0,title:{text:null,reserveSpace:!1,rotation:0},units:[["millisecond",[1,10,100]],["second",[1,10]],["minute",[1,5,15]],["hour",[1,6]],["day",[1]],["week",[1]],["month",[1]],["year",null]]},a),"xAxis"===this.coll&&(D(a.linkedTo)&&!D(a.tickPixelInterval)&&(c.tickPixelInterval=350),D(a.tickPixelInterval)||!D(a.linkedTo)||D(a.tickPositioner)||D(a.tickInterval)||(c.tickPositioner=function(a,h){var b=this.linkedParent&&this.linkedParent.tickPositions&&this.linkedParent.tickPositions.info;if(b){var e=
c.units||[];let f;var d=1;let A="year";for(let a=0;a<e.length;a++){const h=e[a];if(h&&h[0]===b.unitName){f=a;break}}(e=m(f)&&e[f+1])?(A=e[0]||"year",d=(d=e[1])&&d[0]||1):"year"===b.unitName&&(d=10*b.count);b=C[A];this.tickInterval=b*d;return this.chart.time.getTimeTicks({unitRange:b,count:d,unitName:A},a,h,this.options.startOfWeek)}})),w(!0,this.options,c),this.horiz&&(h.minPadding=K(a.minPadding,0),h.maxPadding=K(a.maxPadding,0)),m(h.grid.borderWidth)&&(h.tickWidth=h.lineWidth=b.borderWidth))}function y(a){a=
(a=a.userOptions)&&a.grid||{};const h=a.columns;a.enabled&&h&&w(!0,this.options,h[h.length-1])}function G(){(this.grid.columns||[]).forEach(a=>a.setScale())}function r(a){const {horiz:h,maxLabelDimensions:b,options:{grid:c={}}}=this;if(c.enabled&&b){var d=2*this.options.labels.distance;d=h?c.cellHeight||d+b.height:d+b.width;e(a.tickSize)?a.tickSize[0]=d:a.tickSize=[d,0]}}function c(){this.axes.forEach(a=>{(a.grid&&a.grid.columns||[]).forEach(a=>{a.setAxisSize();a.setAxisTranslation()})})}function I(a){const {grid:h}=
this;(h.columns||[]).forEach(h=>h.destroy(a.keepEvents));h.columns=void 0}function q(a){a=a.userOptions||{};const h=a.grid||{};h.enabled&&D(h.borderColor)&&(a.tickColor=a.lineColor=h.borderColor);this.grid||(this.grid=new P(this));this.hiddenLabels=[];this.hiddenMarks=[]}function f(a){var h=this.label;const b=this.axis;var c=b.reversed,e=b.chart,d=b.options.grid||{};const f=b.options.labels,C=f.align;var l=H[b.side],k=a.tickmarkOffset,p=b.tickPositions;const r=this.pos-k;p=m(p[a.index+1])?p[a.index+
1]-k:(b.max||0)+k;var w=b.tickSize("tick");k=w?w[0]:0;w=w?w[1]/2:0;if(!0===d.enabled){let m;"top"===l?(d=b.top+b.offset,m=d-k):"bottom"===l?(m=e.chartHeight-b.bottom+b.offset,d=m+k):(d=b.top+b.len-(b.translate(c?p:r)||0),m=b.top+b.len-(b.translate(c?r:p)||0));"right"===l?(l=e.chartWidth-b.right+b.offset,c=l+k):"left"===l?(c=b.left+b.offset,l=c-k):(l=Math.round(b.left+(b.translate(c?p:r)||0))-w,c=Math.min(Math.round(b.left+(b.translate(c?r:p)||0))-w,b.left+b.len));this.slotWidth=c-l;a.pos.x="left"===
C?l:"right"===C?c:l+(c-l)/2;a.pos.y=m+(d-m)/2;h&&(e=e.renderer.fontMetrics(h),h=h.getBBox().height,a.pos.y=f.useHTML?a.pos.y+(e.b+-(h/2)):a.pos.y+((e.b-(e.h-e.f))/2+-((Math.round(h/e.h)-1)*e.h/2)));a.pos.x+=b.horiz&&f.x||0}}function l(a){const {axis:b,value:h}=a;if(b.options.grid&&b.options.grid.enabled){var c=b.tickPositions;const e=(b.linkedParent||b).series[0],d=h===c[0];c=h===c[c.length-1];const f=e&&J(e.options.data,function(a){return a[b.isXAxis?"x":"y"]===h});let m;f&&e.is("gantt")&&(m=w(f),
v.seriesTypes.gantt.prototype.pointClass.setGanttPointAliases(m));a.isFirst=d;a.isLast=c;a.point=m}}function p(){const a=this.options,b=this.categories,c=this.tickPositions,e=c[0],d=c[c.length-1],f=this.linkedParent&&this.linkedParent.min||this.min,m=this.linkedParent&&this.linkedParent.max||this.max,l=this.tickInterval;!0!==(a.grid||{}).enabled||b||!this.horiz&&!this.isLinked||(e<f&&e+l>f&&!a.startOnTick&&(c[0]=f),d>m&&d-l<m&&!a.endOnTick&&(c[c.length-1]=m))}function E(a){const {options:{grid:b=
{}}}=this;return!0===b.enabled&&this.categories?this.tickInterval:a.apply(this,Array.prototype.slice.call(arguments,1))}const {dateFormats:k}=v,{addEvent:b,defined:D,erase:d,find:J,isArray:e,isNumber:m,merge:w,pick:K,timeUnits:C,wrap:O}=t;var H;(function(a){a[a.top=0]="top";a[a.right=1]="right";a[a.bottom=2]="bottom";a[a.left=3]="left"})(H||(H={}));const M=[];class P{constructor(a){this.axis=a}isOuterAxis(){const a=this.axis,b=a.grid.columnIndex,c=a.linkedParent&&a.linkedParent.grid.columns||a.grid.columns,
e=b?a.linkedParent:a;let d=-1,f=0;(a.chart[a.coll]||[]).forEach((b,c)=>{b.side!==a.side||b.options.isInternal||(f=c,b===e&&(d=c))});return f===d&&(m(b)?c.length===b:!0)}renderBorder(a){const b=this.axis,c=b.chart.renderer,e=b.options;a=c.path(a).addClass("highcharts-axis-line").add(b.axisBorder);c.styledMode||a.attr({stroke:e.lineColor,"stroke-width":e.lineWidth,zIndex:7});return a}}k.E=function(a){return this.dateFormat("%a",a,!0).charAt(0)};k.W=function(a){const b=this,c=new this.Date(a);["Hours",
"Milliseconds","Minutes","Seconds"].forEach(function(a){b.set(a,c,0)});var e=(this.get("Day",c)+6)%7;a=new this.Date(c.valueOf());this.set("Date",a,this.get("Date",c)-e+3);e=new this.Date(this.get("FullYear",a),0,1);4!==this.get("Day",e)&&(this.set("Month",c,0),this.set("Date",c,1+(11-this.get("Day",e))%7));return(1+Math.floor((a.valueOf()-e.valueOf())/6048E5)).toString()};"";return{compose:function(e,d,m){t.pushUnique(M,e)&&(e.keepProps.push("grid"),e.prototype.getMaxLabelDimensions=F,O(e.prototype,
"unsquish",E),b(e,"init",q),b(e,"afterGetOffset",z),b(e,"afterGetTitlePosition",B),b(e,"afterInit",n),b(e,"afterRender",u),b(e,"afterSetAxisTranslation",x),b(e,"afterSetOptions",a),b(e,"afterSetOptions",y),b(e,"afterSetScale",G),b(e,"afterTickSize",r),b(e,"trimTicks",p),b(e,"destroy",I));t.pushUnique(M,d)&&b(d,"afterSetChartSize",c);t.pushUnique(M,m)&&(b(m,"afterGetLabelPosition",f),b(m,"labelFormat",l));return e}}});z(g,"Gantt/Tree.js",[g["Core/Utilities.js"]],function(g){const {extend:v,isNumber:t,
pick:F}=g,z=function(g,u){const n=g.reduce(function(a,g){const n=F(g.parent,"");"undefined"===typeof a[n]&&(a[n]=[]);a[n].push(g);return a},{});Object.keys(n).forEach(function(a,g){const y=n[a];""!==a&&-1===u.indexOf(a)&&(y.forEach(function(a){g[""].push(a)}),delete g[a])});return n},B=function(g,u,x,a,y,G){let r=0,c=0,n=G&&G.after;var q=G&&G.before;u={data:a,depth:x-1,id:g,level:x,parent:u};let f,l;"function"===typeof q&&q(u,G);q=(y[g]||[]).map(function(a){const p=B(a.id,g,x+1,a,y,G),k=a.start;a=
!0===a.milestone?k:a.end;f=!t(f)||k<f?k:f;l=!t(l)||a>l?a:l;r=r+1+p.descendants;c=Math.max(p.height+1,c);return p});a&&(a.start=F(a.start,f),a.end=F(a.end,l));v(u,{children:q,descendants:r,height:c});"function"===typeof n&&n(u,G);return u};return{getListOfParents:z,getNode:B,getTree:function(g,u){const n=g.map(function(a){return a.id});g=z(g,n);return B("",null,1,null,g,u)}}});z(g,"Core/Axis/TreeGrid/TreeGridTick.js",[g["Core/Utilities.js"]],function(g){function v(){this.treeGrid||(this.treeGrid=new G(this))}
function t(a,c){a=a.treeGrid;const g=!a.labelIcon,q=c.renderer;var f=c.xy;const l=c.options,p=l.width||0,r=l.height||0;var k=f.x-p/2-(l.padding||0);f=f.y-r/2;const b=c.collapsed?90:180,n=c.show&&u(f);let d=a.labelIcon;d||(a.labelIcon=d=q.path(q.symbols[l.type](l.x||0,l.y||0,p,r)).addClass("highcharts-label-icon").add(c.group));d[n?"show":"hide"]();q.styledMode||d.attr({cursor:"pointer",fill:x(c.color,"#666666"),"stroke-width":1,stroke:l.lineColor,strokeWidth:l.lineWidth||0});d[g?"attr":"animate"]({translateX:k,
translateY:f,rotation:b})}function F(a,c,g,q,f,l,p,y,k){var b=x(this.options&&this.options.labels,l);l=this.pos;var r=this.axis;const d="treegrid"===r.options.type;a=a.apply(this,[c,g,q,f,b,p,y,k]);d&&(c=b&&n(b.symbol,!0)?b.symbol:{},b=b&&u(b.indentation)?b.indentation:0,l=(l=(r=r.treeGrid.mapOfPosToGridNode)&&r[l])&&l.depth||1,a.x+=(c.width||0)+2*(c.padding||0)+(l-1)*b);return a}function z(a){const c=this;var g=c.pos,q=c.axis;const f=c.label;var l=q.treeGrid.mapOfPosToGridNode,p=q.options;const r=
x(c.options&&c.options.labels,p&&p.labels);var k=r&&n(r.symbol,!0)?r.symbol:{};const b=(l=l&&l[g])&&l.depth;p="treegrid"===p.type;const y=-1<q.tickPositions.indexOf(g);g=q.chart.styledMode;p&&l&&f&&f.element&&f.addClass("highcharts-treegrid-node-level-"+b);a.apply(c,Array.prototype.slice.call(arguments,1));p&&f&&f.element&&l&&l.descendants&&0<l.descendants&&(q=q.treeGrid.isCollapsed(l),t(c,{color:!g&&f.styles&&f.styles.color||"",collapsed:q,group:f.parentGroup,options:k,renderer:f.renderer,show:y,
xy:f.xy}),k="highcharts-treegrid-node-"+(q?"expanded":"collapsed"),f.addClass("highcharts-treegrid-node-"+(q?"collapsed":"expanded")).removeClass(k),g||f.css({cursor:"pointer"}),[f,c.treeGrid.labelIcon].forEach(a=>{a&&!a.attachedTreeGridEvents&&(B(a.element,"mouseover",function(){f.addClass("highcharts-treegrid-node-active");f.renderer.styledMode||f.css({textDecoration:"underline"})}),B(a.element,"mouseout",function(){{const a=n(r.style)?r.style:{};f.removeClass("highcharts-treegrid-node-active");
f.renderer.styledMode||f.css({textDecoration:a.textDecoration})}}),B(a.element,"click",function(){c.treeGrid.toggleCollapse()}),a.attachedTreeGridEvents=!0)}))}const {addEvent:B,isObject:n,isNumber:u,pick:x,wrap:a}=g,y=[];class G{static compose(r){g.pushUnique(y,r)&&(B(r,"init",v),a(r.prototype,"getLabelPosition",F),a(r.prototype,"renderLabel",z),r.prototype.collapse=function(a){this.treeGrid.collapse(a)},r.prototype.expand=function(a){this.treeGrid.expand(a)},r.prototype.toggleCollapse=function(a){this.treeGrid.toggleCollapse(a)})}constructor(a){this.tick=
a}collapse(a){var c=this.tick;const g=c.axis,q=g.brokenAxis;q&&g.treeGrid.mapOfPosToGridNode&&(c=g.treeGrid.collapse(g.treeGrid.mapOfPosToGridNode[c.pos]),q.setBreaks(c,x(a,!0)))}destroy(){this.labelIcon&&this.labelIcon.destroy()}expand(a){var c=this.tick;const g=c.axis,q=g.brokenAxis;q&&g.treeGrid.mapOfPosToGridNode&&(c=g.treeGrid.expand(g.treeGrid.mapOfPosToGridNode[c.pos]),q.setBreaks(c,x(a,!0)))}toggleCollapse(a){var c=this.tick;const g=c.axis,q=g.brokenAxis;q&&g.treeGrid.mapOfPosToGridNode&&
(c=g.treeGrid.toggleCollapse(g.treeGrid.mapOfPosToGridNode[c.pos]),q.setBreaks(c,x(a,!0)))}}return G});z(g,"Series/TreeUtilities.js",[g["Core/Color/Color.js"],g["Core/Utilities.js"]],function(g,v){function t(a,g){var n=g.before;const r=g.idRoot,c=g.mapIdToNode[r],y=g.points[a.i],q=y&&y.options||{},f=[];let l=0;a.levelDynamic=a.level-(!1!==g.levelIsConstant?0:c.level);a.name=x(y&&y.name,"");a.visible=r===a.id||!0===g.visible;"function"===typeof n&&(a=n(a,g));a.children.forEach((c,q)=>{const k=z({},
g);z(k,{index:q,siblings:a.children.length,visible:a.visible});c=t(c,k);f.push(c);c.visible&&(l+=c.val)});n=x(q.value,l);a.visible=0<=n&&(0<l||a.visible);a.children=f;a.childrenTotal=l;a.isLeaf=a.visible&&!l;a.val=n;return a}const {extend:z,isArray:F,isNumber:B,isObject:n,merge:u,pick:x}=v;return{getColor:function(a,n){const y=n.index;var r=n.mapOptionsToLevel;const c=n.parentColor,u=n.parentColorIndex,q=n.series;var f=n.colors;const l=n.siblings;var p=q.points,t=q.chart.options.chart;let k;var b;
let v;if(a){p=p[a.i];a=r[a.level]||{};if(r=p&&a.colorByPoint){k=p.index%(f?f.length:t.colorCount);var d=f&&f[k]}if(!q.chart.styledMode){f=p&&p.options.color;t=a&&a.color;if(b=c)b=(b=a&&a.colorVariation)&&"brightness"===b.key&&y&&l?g.parse(c).brighten(y/l*b.to).get():c;b=x(f,t,d,b,q.color)}v=x(p&&p.options.colorIndex,a&&a.colorIndex,k,u,n.colorIndex)}return{color:b,colorIndex:v}},getLevelOptions:function(a){let g={},t,r,c;if(n(a)){c=B(a.from)?a.from:1;var v=a.levels;r={};t=n(a.defaults)?a.defaults:
{};F(v)&&(r=v.reduce((a,f)=>{let g,p;n(f)&&B(f.level)&&(p=u({},f),g=x(p.levelIsConstant,t.levelIsConstant),delete p.levelIsConstant,delete p.level,f=f.level+(g?0:c-1),n(a[f])?u(!0,a[f],p):a[f]=p);return a},{}));v=B(a.to)?a.to:1;for(a=0;a<=v;a++)g[a]=u({},t,n(r[a])?r[a]:{})}return g},setTreeValues:t,updateRootId:function(a){if(n(a)){var g=n(a.options)?a.options:{};g=x(a.rootNode,g.rootId,"");n(a.userOptions)&&(a.userOptions.rootId=g);a.rootNode=g}return g}}});z(g,"Core/Axis/TreeGrid/TreeGridAxis.js",
[g["Core/Axis/BrokenAxis.js"],g["Core/Axis/GridAxis.js"],g["Gantt/Tree.js"],g["Core/Axis/TreeGrid/TreeGridTick.js"],g["Series/TreeUtilities.js"],g["Core/Utilities.js"]],function(g,v,t,z,N,B){function n(a,b){const c=a.collapseEnd||0;a=a.collapseStart||0;c>=b&&(a-=.5);return{from:a,to:c,showPoints:!1}}function u(a,b,c){const e=[],d=[],f={},g="boolean"===typeof b?b:!1;let m={},k=-1;a=t.getTree(a,{after:function(a){a=m[a.pos];let b=0,c=0;a.children.forEach(function(a){c+=(a.descendants||0)+1;b=Math.max((a.height||
0)+1,b)});a.descendants=c;a.height=b;a.collapsed&&d.push(a)},before:function(a){const b=l(a.data,!0)?a.data:{},c=p(b.name)?b.name:"";var d=f[a.parent];d=l(d,!0)?m[d.pos]:null;var h=function(a){return a.name===c};let C;g&&l(d,!0)&&(C=I(d.children,h))?(h=C.pos,C.nodes.push(a)):h=k++;m[h]||(m[h]=C={depth:d?d.depth+1:0,name:c,id:b.id,nodes:[a],children:[],pos:h},-1!==h&&e.push(c),l(d,!0)&&d.children.push(C));p(a.id)&&(f[a.id]=a);C&&!0===b.collapsed&&(C.collapsed=!0);a.pos=h}});m=function(a,b){const c=
function(a,e,d){let f=e+(-1===e?0:b-1);const g=(f-e)/2,h=e+g;a.nodes.forEach(function(a){const b=a.data;l(b,!0)&&(b.y=e+(b.seriesIndex||0),delete b.seriesIndex);a.pos=h});d[h]=a;a.pos=h;a.tickmarkOffset=g+.5;a.collapseStart=f+.5;a.children.forEach(function(a){c(a,f+1,d);f=(a.collapseEnd||0)-.5});a.collapseEnd=f+.5;return d};return c(a["-1"],-1,{})}(m,c);return{categories:e,mapOfIdToNode:f,mapOfPosToGridNode:m,collapsedNodes:d,tree:a}}function x(a){a.target.axes.filter(function(a){return"treegrid"===
a.options.type}).forEach(function(b){var c=b.options||{};const e=c.labels,d=c.uniqueNames;c=c.max;let g=0,m;if(!b.treeGrid.mapOfPosToGridNode||b.series.some(function(a){return!a.hasRendered||a.isDirtyData||a.isDirty})){m=b.series.reduce(function(a,b){b.visible&&((b.options.data||[]).forEach(function(c){b.options.keys&&b.options.keys.length&&(c=b.pointClass.prototype.optionsToObject.call({series:b},c),b.pointClass.setGanttPointAliases(c));l(c,!0)&&(c.seriesIndex=g,a.push(c))}),!0===d&&g++);return a},
[]);if(c&&m.length<c)for(let a=m.length;a<=c;a++)m.push({name:a+"\u200b"});c=u(m,d||!1,!0===d?g:1);b.categories=c.categories;b.treeGrid.mapOfPosToGridNode=c.mapOfPosToGridNode;b.hasNames=!0;b.treeGrid.tree=c.tree;b.series.forEach(function(a){const b=(a.options.data||[]).map(function(b){f(b)&&a.options.keys&&a.options.keys.length&&m.forEach(function(a){0<=b.indexOf(a.x)&&0<=b.indexOf(a.x2)&&(b=a)});return l(b,!0)?E(b):b});a.visible&&a.setData(b,!1)});b.treeGrid.mapOptionsToLevel=r({defaults:e,from:1,
levels:e&&e.levels,to:b.treeGrid.tree&&b.treeGrid.tree.height});"beforeRender"===a.type&&(b.treeGrid.collapsedNodes=c.collapsedNodes)}})}function a(a,b){var c=this.treeGrid.mapOptionsToLevel||{};const e=this.ticks;let f=e[b],g,m;"treegrid"===this.options.type&&this.treeGrid.mapOfPosToGridNode?(m=this.treeGrid.mapOfPosToGridNode[b],(c=c[m.depth])&&(g={labels:c}),!f&&d?e[b]=new d(this,b,void 0,void 0,{category:m.name,tickmarkOffset:m.tickmarkOffset,options:g}):(f.parameters.category=m.name,f.options=
g,f.addLabel())):a.apply(this,Array.prototype.slice.call(arguments,1))}function y(a,b,d,f){const e=this,g="treegrid"===d.type;e.treeGrid||(e.treeGrid=new J(e));g&&(c(b,"beforeRender",x),c(b,"beforeRedraw",x),c(b,"addSeries",function(a){a.options.data&&(a=u(a.options.data,d.uniqueNames||!1,1),e.treeGrid.collapsedNodes=(e.treeGrid.collapsedNodes||[]).concat(a.collapsedNodes))}),c(e,"foundExtremes",function(){e.treeGrid.collapsedNodes&&e.treeGrid.collapsedNodes.forEach(function(a){const b=e.treeGrid.collapse(a);
e.brokenAxis&&(e.brokenAxis.setBreaks(b,!1),e.treeGrid.collapsedNodes&&(e.treeGrid.collapsedNodes=e.treeGrid.collapsedNodes.filter(b=>a.collapseStart!==b.collapseStart||a.collapseEnd!==b.collapseEnd)))})}),c(e,"afterBreaks",function(){"yAxis"===e.coll&&!e.staticScale&&e.chart.options.chart.height&&(e.isDirty=!0)}),d=E({grid:{enabled:!0},labels:{align:"left",levels:[{level:void 0},{level:1,style:{fontWeight:"bold"}}],symbol:{type:"triangle",x:-5,y:-5,height:10,width:10,padding:5}},uniqueNames:!1},
d,{reversed:!0,grid:{columns:void 0}}));a.apply(e,[b,d,f]);g&&(e.hasNames=!0,e.options.showLastLabel=!0)}function F(a){const b=this.options;"treegrid"===b.type?(this.min=k(this.userMin,b.min,this.dataMin),this.max=k(this.userMax,b.max,this.dataMax),q(this,"foundExtremes"),this.setAxisTranslation(),this.tickmarkOffset=.5,this.tickInterval=1,this.tickPositions=this.treeGrid.mapOfPosToGridNode?this.treeGrid.getTickPositions():[]):a.apply(this,Array.prototype.slice.call(arguments,1))}const {getLevelOptions:r}=
N,{addEvent:c,find:I,fireEvent:q,isArray:f,isObject:l,isString:p,merge:E,pick:k,wrap:b}=B,D=[];let d;class J{static compose(c,f,l,k){if(B.pushUnique(D,c)){-1===c.keepProps.indexOf("treeGrid")&&c.keepProps.push("treeGrid");const e=c.prototype;b(e,"generateTick",a);b(e,"init",y);b(e,"setTickInterval",F);e.utils={getNode:t.getNode}}B.pushUnique(D,k)&&(d||(d=k));v.compose(c,f,k);g.compose(c,l);z.compose(k);return c}constructor(a){this.axis=a}setCollapsedStatus(a){const b=this.axis,c=b.chart;b.series.forEach(function(b){const e=
b.options.data;if(a.id&&e){const d=c.get(a.id);b=e[b.data.indexOf(d)];d&&b&&(d.collapsed=a.collapsed,b.collapsed=a.collapsed)}})}collapse(a){const b=this.axis,c=b.options.breaks||[],e=n(a,b.max);c.push(e);a.collapsed=!0;b.treeGrid.setCollapsedStatus(a);return c}expand(a){const b=this.axis,c=b.options.breaks||[],e=n(a,b.max);a.collapsed=!1;b.treeGrid.setCollapsedStatus(a);return c.reduce(function(a,b){b.to===e.to&&b.from===e.from||a.push(b);return a},[])}getTickPositions(){const a=this.axis,b=Math.floor(a.min/
a.tickInterval)*a.tickInterval,c=Math.ceil(a.max/a.tickInterval)*a.tickInterval;return Object.keys(a.treeGrid.mapOfPosToGridNode||{}).reduce(function(e,d){d=+d;!(d>=b&&d<=c)||a.brokenAxis&&a.brokenAxis.isInAnyBreak(d)||e.push(d);return e},[])}isCollapsed(a){const b=this.axis,c=b.options.breaks||[],d=n(a,b.max);return c.some(function(a){return a.from===d.from&&a.to===d.to})}toggleCollapse(a){return this.isCollapsed(a)?this.expand(a):this.collapse(a)}}return J});z(g,"masters/modules/treegrid.src.js",
[g["Core/Globals.js"],g["Core/Axis/TreeGrid/TreeGridAxis.js"]],function(g,v){v.compose(g.Axis,g.Chart,g.Series,g.Tick)})});
//# sourceMappingURL=treegrid.js.map