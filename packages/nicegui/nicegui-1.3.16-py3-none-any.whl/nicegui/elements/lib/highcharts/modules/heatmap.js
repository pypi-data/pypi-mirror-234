/*
 Highmaps JS v11.1.0 (2023-06-05)

 (c) 2009-2021 Torstein Honsi

 License: www.highcharts.com/license
*/
'use strict';(function(b){"object"===typeof module&&module.exports?(b["default"]=b,module.exports=b):"function"===typeof define&&define.amd?define("highcharts/modules/heatmap",["highcharts"],function(u){b(u);b.Highcharts=u;return b}):b("undefined"!==typeof Highcharts?Highcharts:void 0)})(function(b){function u(b,k,x,D){b.hasOwnProperty(k)||(b[k]=D.apply(null,x),"function"===typeof CustomEvent&&window.dispatchEvent(new CustomEvent("HighchartsModuleLoaded",{detail:{path:k,module:b[k]}})))}b=b?b._modules:
{};u(b,"Core/Axis/Color/ColorAxisComposition.js",[b["Core/Color/Color.js"],b["Core/Utilities.js"]],function(b,k){const {parse:x}=b,{addEvent:n,extend:v,merge:y,pick:A,splat:g}=k;var p;(function(b){function p(){const a=this.options;this.colorAxis=[];a.colorAxis&&(a.colorAxis=g(a.colorAxis),a.colorAxis.forEach(a=>{new f(this,a)}))}function E(a){const e=c=>{c=a.allItems.indexOf(c);-1!==c&&(this.destroyItem(a.allItems[c]),a.allItems.splice(c,1))};let c=[],l,d;(this.chart.colorAxis||[]).forEach(function(a){(l=
a.options)&&l.showInLegend&&(l.dataClasses&&l.visible?c=c.concat(a.getDataClassLegendSymbols()):l.visible&&c.push(a),a.series.forEach(function(a){if(!a.options.showInLegend||l.dataClasses)"point"===a.options.legendType?a.points.forEach(function(a){e(a)}):e(a)}))});for(d=c.length;d--;)a.allItems.unshift(c[d])}function w(a){a.visible&&a.item.legendColor&&a.item.legendItem.symbol.attr({fill:a.item.legendColor})}function r(){const a=this.chart.colorAxis;a&&a.forEach(function(a,c,e){a.update({},e)})}function q(){(this.chart.colorAxis&&
this.chart.colorAxis.length||this.colorAttribs)&&this.translateColors()}function c(){const a=this.axisTypes;a?-1===a.indexOf("colorAxis")&&a.push("colorAxis"):this.axisTypes=["colorAxis"]}function a(a){const c=this,e=a?"show":"hide";c.visible=c.options.visible=!!a;["graphic","dataLabel"].forEach(function(a){if(c[a])c[a][e]()});this.series.buildKDTree()}function m(){const a=this,c=this.options.nullColor,e=this.colorAxis,d=this.colorKey;(this.data.length?this.data:this.points).forEach(f=>{var h=f.getNestedProperty(d);
(h=f.options.color||(f.isNull||null===f.value?c:e&&"undefined"!==typeof h?e.toColor(h,f):f.color||a.color))&&f.color!==h&&(f.color=h,"point"===a.options.legendType&&f.legendItem&&f.legendItem.label&&a.chart.legend.colorizeItem(f,f.visible))})}function d(a){const c=a.prototype.createAxis;a.prototype.createAxis=function(a,e){if("colorAxis"!==a)return c.apply(this,arguments);const d=new f(this,y(e.axis,{index:this[a].length,isX:!1}));this.isDirtyLegend=!0;this.axes.forEach(function(a){a.series=[]});
this.series.forEach(function(a){a.bindAxes();a.isDirtyData=!0});A(e.redraw,!0)&&this.redraw(e.animation);return d}}function C(){this.elem.attr("fill",x(this.start).tweenTo(x(this.end),this.pos),void 0,!0)}function e(){this.elem.attr("stroke",x(this.start).tweenTo(x(this.end),this.pos),void 0,!0)}const h=[];let f;b.compose=function(l,b,B,z,g){f||(f=l);k.pushUnique(h,b)&&(l=b.prototype,l.collectionsWithUpdate.push("colorAxis"),l.collectionsWithInit.colorAxis=[l.addColorAxis],n(b,"afterGetAxes",p),d(b));
k.pushUnique(h,B)&&(b=B.prototype,b.fillSetter=C,b.strokeSetter=e);k.pushUnique(h,z)&&(n(z,"afterGetAllItems",E),n(z,"afterColorizeItem",w),n(z,"afterUpdate",r));k.pushUnique(h,g)&&(v(g.prototype,{optionalAxis:"colorAxis",translateColors:m}),v(g.prototype.pointClass.prototype,{setVisible:a}),n(g,"afterTranslate",q,{order:1}),n(g,"bindAxes",c))};b.pointSetVisible=a})(p||(p={}));return p});u(b,"Core/Axis/Color/ColorAxisDefaults.js",[],function(){return{lineWidth:0,minPadding:0,maxPadding:0,gridLineColor:"#ffffff",
gridLineWidth:1,tickPixelInterval:72,startOnTick:!0,endOnTick:!0,offset:0,marker:{animation:{duration:50},width:.01,color:"#999999"},labels:{distance:8,overflow:"justify",rotation:0},minColor:"#e6e9ff",maxColor:"#0022ff",tickLength:5,showInLegend:!0}});u(b,"Core/Axis/Color/ColorAxis.js",[b["Core/Axis/Axis.js"],b["Core/Color/Color.js"],b["Core/Axis/Color/ColorAxisComposition.js"],b["Core/Axis/Color/ColorAxisDefaults.js"],b["Core/Legend/LegendSymbol.js"],b["Core/Series/SeriesRegistry.js"],b["Core/Utilities.js"]],
function(b,k,x,u,v,y,A){const {parse:g}=k,{series:p}=y,{extend:E,isArray:n,isNumber:t,merge:w,pick:r}=A;class q extends b{static compose(c,a,m,d){x.compose(q,c,a,m,d)}constructor(c,a){super(c,a);this.beforePadding=!1;this.chart=void 0;this.coll="colorAxis";this.stops=this.options=this.dataClasses=void 0;this.visible=!0;this.init(c,a)}init(c,a){var m=c.options.legend||{};const d=a.layout?"vertical"!==a.layout:"vertical"!==m.layout,b=a.visible;m=w(q.defaultColorAxisOptions,a,{showEmpty:!1,title:null,
visible:m.enabled&&!1!==b});this.side=a.side||d?2:1;this.reversed=a.reversed||!d;this.opposite=!d;super.init(c,m,"colorAxis");this.userOptions=a;n(c.userOptions.colorAxis)&&(c.userOptions.colorAxis[this.index]=a);a.dataClasses&&this.initDataClasses(a);this.initStops();this.horiz=d;this.zoomEnabled=!1}initDataClasses(c){const a=this.chart,m=this.legendItem=this.legendItem||{},d=c.dataClasses.length,b=this.options;let e,h=0,f=a.options.chart.colorCount;this.dataClasses=e=[];m.labels=[];(c.dataClasses||
[]).forEach(function(c,m){c=w(c);e.push(c);if(a.styledMode||!c.color)"category"===b.dataClassColor?(a.styledMode||(m=a.options.colors,f=m.length,c.color=m[h]),c.colorIndex=h,h++,h===f&&(h=0)):c.color=g(b.minColor).tweenTo(g(b.maxColor),2>d?.5:m/(d-1))})}hasData(){return!!(this.tickPositions||[]).length}setTickPositions(){if(!this.dataClasses)return super.setTickPositions()}initStops(){this.stops=this.options.stops||[[0,this.options.minColor],[1,this.options.maxColor]];this.stops.forEach(function(c){c.color=
g(c[1])})}setOptions(c){super.setOptions(c);this.options.crosshair=this.options.marker}setAxisSize(){var c=this.legendItem&&this.legendItem.symbol;const a=this.chart;var m=a.options.legend||{};let d,b;c?(this.left=m=c.attr("x"),this.top=d=c.attr("y"),this.width=b=c.attr("width"),this.height=c=c.attr("height"),this.right=a.chartWidth-m-b,this.bottom=a.chartHeight-d-c,this.len=this.horiz?b:c,this.pos=this.horiz?m:d):this.len=(this.horiz?m.symbolWidth:m.symbolHeight)||q.defaultLegendLength}normalizedValue(c){this.logarithmic&&
(c=this.logarithmic.log2lin(c));return 1-(this.max-c)/(this.max-this.min||1)}toColor(c,a){const m=this.dataClasses;var d=this.stops;let b,e,h,f;if(m)for(f=m.length;f--;){if(h=m[f],b=h.from,d=h.to,("undefined"===typeof b||c>=b)&&("undefined"===typeof d||c<=d)){e=h.color;a&&(a.dataClass=f,a.colorIndex=h.colorIndex);break}}else{c=this.normalizedValue(c);for(f=d.length;f--&&!(c>d[f][0]););b=d[f]||d[f+1];d=d[f+1]||b;c=1-(d[0]-c)/(d[0]-b[0]||1);e=b.color.tweenTo(d.color,c)}return e}getOffset(){const c=
this.legendItem&&this.legendItem.group,a=this.chart.axisOffset[this.side];if(c){this.axisParent=c;super.getOffset();const b=this.chart.legend;b.allItems.forEach(function(a){a instanceof q&&a.drawLegendSymbol(b,a)});b.render();this.chart.getMargins(!0);this.added||(this.added=!0,this.labelLeft=0,this.labelRight=this.width);this.chart.axisOffset[this.side]=a}}setLegendColor(){var c=this.reversed,a=c?1:0;c=c?0:1;a=this.horiz?[a,0,c,0]:[0,c,0,a];this.legendColor={linearGradient:{x1:a[0],y1:a[1],x2:a[2],
y2:a[3]},stops:this.stops}}drawLegendSymbol(c,a){var b;a=a.legendItem||{};const d=c.padding,g=c.options,e=this.options.labels,h=r(g.itemDistance,10),f=this.horiz,l=r(g.symbolWidth,f?q.defaultLegendLength:12),p=r(g.symbolHeight,f?12:q.defaultLegendLength),B=r(g.labelPadding,f?16:30);this.setLegendColor();a.symbol||(a.symbol=this.chart.renderer.symbol("roundedRect",0,c.baseline-11,l,p,{r:null!==(b=g.symbolRadius)&&void 0!==b?b:3}).attr({zIndex:1}).add(a.group));a.labelWidth=l+d+(f?h:r(e.x,e.distance)+
this.maxLabelLength);a.labelHeight=p+d+(f?B:0)}setState(c){this.series.forEach(function(a){a.setState(c)})}setVisible(){}getSeriesExtremes(){const c=this.series;let a;let b,d,g=c.length,e,h;this.dataMin=Infinity;for(this.dataMax=-Infinity;g--;){d=c[g];a=d.colorKey=r(d.options.colorKey,d.colorKey,d.pointValKey,d.zoneAxis,"y");var f=d.pointArrayMap;b=d[a+"Min"]&&d[a+"Max"];if(d[a+"Data"])var l=d[a+"Data"];else if(f){if(l=[],f=f.indexOf(a),e=d.yData,0<=f&&e)for(h=0;h<e.length;h++)l.push(r(e[h][f],e[h]))}else l=
d.yData;b?(d.minColorValue=d[a+"Min"],d.maxColorValue=d[a+"Max"]):(l=p.prototype.getExtremes.call(d,l),d.minColorValue=l.dataMin,d.maxColorValue=l.dataMax);"undefined"!==typeof d.minColorValue&&(this.dataMin=Math.min(this.dataMin,d.minColorValue),this.dataMax=Math.max(this.dataMax,d.maxColorValue));b||p.prototype.applyExtremes.call(d)}}drawCrosshair(c,a){const b=this.legendItem||{},d=a&&a.plotX,g=a&&a.plotY,e=this.pos,h=this.len;let f;a&&(f=this.toPixels(a.getNestedProperty(a.series.colorKey)),f<
e?f=e-2:f>e+h&&(f=e+h+2),a.plotX=f,a.plotY=this.len-f,super.drawCrosshair(c,a),a.plotX=d,a.plotY=g,this.cross&&!this.cross.addedToColorAxis&&b.group&&(this.cross.addClass("highcharts-coloraxis-marker").add(b.group),this.cross.addedToColorAxis=!0,this.chart.styledMode||"object"!==typeof this.crosshair||this.cross.attr({fill:this.crosshair.color})))}getPlotLinePath(c){const a=this.left,b=c.translatedValue,d=this.top;return t(b)?this.horiz?[["M",b-4,d-6],["L",b+4,d-6],["L",b,d],["Z"]]:[["M",a,b],["L",
a-6,b+6],["L",a-6,b-6],["Z"]]:super.getPlotLinePath(c)}update(c,a){const b=this.chart.legend;this.series.forEach(a=>{a.isDirtyData=!0});(c.dataClasses&&b.allItems||this.dataClasses)&&this.destroyItems();super.update(c,a);this.legendItem&&this.legendItem.label&&(this.setLegendColor(),b.colorizeItem(this,!0))}destroyItems(){const c=this.chart,a=this.legendItem||{};if(a.label)c.legend.destroyItem(this);else if(a.labels)for(const b of a.labels)c.legend.destroyItem(b);c.isDirtyLegend=!0}destroy(){this.chart.isDirtyLegend=
!0;this.destroyItems();super.destroy(...[].slice.call(arguments))}remove(c){this.destroyItems();super.remove(c)}getDataClassLegendSymbols(){const c=this,a=c.chart,b=c.legendItem&&c.legendItem.labels||[],d=a.options.legend,g=r(d.valueDecimals,-1),e=r(d.valueSuffix,""),h=a=>c.series.reduce((c,e)=>{c.push(...e.points.filter(c=>c.dataClass===a));return c},[]);let f;b.length||c.dataClasses.forEach((d,m)=>{const l=d.from,z=d.to,{numberFormatter:p}=a;let k=!0;f="";"undefined"===typeof l?f="< ":"undefined"===
typeof z&&(f="> ");"undefined"!==typeof l&&(f+=p(l,g)+e);"undefined"!==typeof l&&"undefined"!==typeof z&&(f+=" - ");"undefined"!==typeof z&&(f+=p(z,g)+e);b.push(E({chart:a,name:f,options:{},drawLegendSymbol:v.rectangle,visible:!0,isDataClass:!0,setState:a=>{for(const c of h(m))c.setState(a)},setVisible:function(){this.visible=k=c.visible=!k;for(const a of h(m))a.setVisible(k);a.legend.colorizeItem(this,k)}},d))});return b}}q.defaultColorAxisOptions=u;q.defaultLegendLength=200;q.keepProps=["legendItem"];
Array.prototype.push.apply(b.keepProps,q.keepProps);"";return q});u(b,"Series/ColorMapComposition.js",[b["Core/Series/SeriesRegistry.js"],b["Core/Utilities.js"]],function(b,k){const {column:{prototype:n}}=b.seriesTypes,{addEvent:u,defined:v}=k;var y;(function(b){function g(b){this.moveToTopOnHover&&this.graphic&&this.graphic.attr({zIndex:b&&"hover"===b.state?1:0})}const p=[];b.pointMembers={dataLabelOnNull:!0,moveToTopOnHover:!0,isValid:function(){return null!==this.value&&Infinity!==this.value&&
-Infinity!==this.value&&(void 0===this.value||!isNaN(this.value))}};b.seriesMembers={colorKey:"value",axisTypes:["xAxis","yAxis","colorAxis"],parallelArrays:["x","y","value"],pointArrayMap:["value"],trackerGroups:["group","markerGroup","dataLabelsGroup"],colorAttribs:function(b){const g={};!v(b.color)||b.state&&"normal"!==b.state||(g[this.colorProp||"fill"]=b.color);return g},pointAttribs:n.pointAttribs};b.compose=function(b){const n=b.prototype.pointClass;k.pushUnique(p,n)&&u(n,"afterSetState",g);
return b}})(y||(y={}));return y});u(b,"Series/Heatmap/HeatmapPoint.js",[b["Core/Series/SeriesRegistry.js"],b["Core/Utilities.js"]],function(b,k){({seriesTypes:{scatter:{prototype:{pointClass:b}}}}=b);const {clamp:n,defined:u,extend:v,pick:y}=k;class A extends b{constructor(){super(...arguments);this.y=this.x=this.value=this.series=this.options=void 0}applyOptions(b,p){(this.isNull||null===this.value)&&delete this.color;super.applyOptions(b,p);this.formatPrefix=this.isNull||null===this.value?"null":
"point";return this}getCellAttributes(){var b=this.series;const p=b.options,k=(p.colsize||1)/2,v=(p.rowsize||1)/2,t=b.xAxis,w=b.yAxis,r=this.options.marker||b.options.marker;b=b.pointPlacementToXValue();const q=y(this.pointPadding,p.pointPadding,0),c={x1:n(Math.round(t.len-t.translate(this.x-k,!1,!0,!1,!0,-b)),-t.len,2*t.len),x2:n(Math.round(t.len-t.translate(this.x+k,!1,!0,!1,!0,-b)),-t.len,2*t.len),y1:n(Math.round(w.translate(this.y-v,!1,!0,!1,!0)),-w.len,2*w.len),y2:n(Math.round(w.translate(this.y+
v,!1,!0,!1,!0)),-w.len,2*w.len)};[["width","x"],["height","y"]].forEach(function(a){var b=a[0];a=a[1];let d=a+"1",g=a+"2";const e=Math.abs(c[d]-c[g]),h=r&&r.lineWidth||0,f=Math.abs(c[d]+c[g])/2;b=r&&r[b];u(b)&&b<e&&(b=b/2+h/2,c[d]=f-b,c[g]=f+b);if(q){if("x"===a&&t.reversed||"y"===a&&!w.reversed)d=g,g=a+"1";c[d]+=q;c[g]-=q}});return c}haloPath(b){if(!b)return[];const {x:g=0,y:k=0,width:n=0,height:t=0}=this.shapeArgs||{};return[["M",g-b,k-b],["L",g-b,k+t+b],["L",g+n+b,k+t+b],["L",g+n+b,k-b],["Z"]]}isValid(){return Infinity!==
this.value&&-Infinity!==this.value}}v(A.prototype,{dataLabelOnNull:!0,moveToTopOnHover:!0,ttBelow:!1});return A});u(b,"Series/Heatmap/HeatmapSeries.js",[b["Core/Color/Color.js"],b["Series/ColorMapComposition.js"],b["Core/Globals.js"],b["Series/Heatmap/HeatmapPoint.js"],b["Core/Series/SeriesRegistry.js"],b["Core/Renderer/SVG/SVGRenderer.js"],b["Core/Utilities.js"]],function(b,k,u,D,v,y,A){const {doc:g}=u,{series:p,seriesTypes:{column:n,scatter:x}}=v,{prototype:{symbols:t}}=y,{clamp:w,extend:r,fireEvent:q,
isNumber:c,merge:a,pick:m,defined:d}=A;class C extends x{constructor(){super(...arguments);this.points=this.options=this.data=this.context=this.colorAxis=this.canvas=void 0;this.valueMin=this.valueMax=NaN}drawPoints(){const a=this;var b=a.options,c=b.marker||{};if(b.interpolation){const {image:e,chart:f,xAxis:h,yAxis:n,points:p}=a;c=p.length-1;const {len:B,reversed:t}=h,{len:q,reversed:u}=n,{min:r,max:v}=h.getExtremes(),{min:x,max:y}=n.getExtremes(),[A,C]=[m(b.colsize,1),m(b.rowsize,1)];var l=f.inverted,
g=A/2;b=h.userOptions.minPadding;var k=d(b)&&!(0<b);b=l||k;g=k&&g||0;const [F,D,E]=[r-g,v+2*g,r+A].map(b=>w(Math.round(h.len-h.translate(b,!1,!0,!1,!0,-a.pointPlacementToXValue())),-h.len,2*h.len)),[I,J]=t?[D,F]:[F,D];g=B/E/2/2/2;l=l?{width:B,height:q,x:0,y:0}:{x:I-g,width:J-g,height:q,y:0};if(!e||a.isDirtyData){const d=f.colorAxis&&f.colorAxis[0];g=a.getContext();if((k=a.canvas)&&g&&d){const h=k.width=~~((v-r)/A)+1,z=k.height=~~((y-x)/C)+1,n=h*z,B=new Uint8ClampedArray(4*n),q=h-(b&&1||0),w=z-1;b=
a=>{a=d.toColor(a.value||0,m(a)).split(")")[0].split("(")[1].split(",").map(a=>m(parseFloat(a),parseInt(a,10)));a[3]=255*m(a[3],1);return a};const F=t?a=>q-a:a=>a,G=u?a=>w-a:a=>a,H=(a,b)=>Math.ceil(h*G(~~((w-0)/(y-x)*(y-b-x)))+F(~~((q-0)/(v-r)*(a-r))));a.buildKDTree();a.directTouch=!1;for(let a=0;a<n;a++){const e=p[~~((c-0)/(B.length-4)*a*4)],d=new Uint8ClampedArray(b(e));B.set(d,4*H(e.x,e.y))}g.putImageData(new ImageData(B,h,z),0,0);e?e.attr(Object.assign(Object.assign({},l),{href:k.toDataURL()})):
a.image=f.renderer.image(k.toDataURL()).attr(l).add(a.group)}}else e.width===l.width&&e.height===l.height||e.attr(l)}else if(c.enabled||a._hasPointMarkers)p.prototype.drawPoints.call(a),a.points.forEach(b=>{b.graphic&&(b.graphic[a.chart.styledMode?"css":"animate"](a.colorAttribs(b)),null===b.value&&b.graphic.addClass("highcharts-null-point"))})}getContext(){const {canvas:a,context:b}=this;if(a&&b)b.clearRect(0,0,a.width,a.height);else return this.canvas=g.createElement("canvas"),this.context=this.canvas.getContext("2d")||
void 0;return b}getExtremes(){const {dataMin:a,dataMax:b}=p.prototype.getExtremes.call(this,this.valueData);c(a)&&(this.valueMin=a);c(b)&&(this.valueMax=b);return p.prototype.getExtremes.call(this)}getValidPoints(a,b){return p.prototype.getValidPoints.call(this,a,b,!0)}hasData(){return!!this.processedXData.length}init(){super.init.apply(this,arguments);const a=this.options;a.pointRange=m(a.pointRange,a.colsize||1);this.yAxis.axisPointRange=a.rowsize||1;t.ellipse=t.circle;a.marker&&c(a.borderRadius)&&
(a.marker.r=a.borderRadius)}markerAttribs(a,b){const c=a.shapeArgs||{};if(a.hasImage)return{x:a.plotX,y:a.plotY};if(b&&"normal"!==b){var d=a.options.marker||{};a=this.options.marker||{};a=a.states&&a.states[b]||{};d=d.states&&d.states[b]||{};b=(d.width||a.width||c.width||0)+(d.widthPlus||a.widthPlus||0);a=(d.height||a.height||c.height||0)+(d.heightPlus||a.heightPlus||0);return{x:(c.x||0)+((c.width||0)-b)/2,y:(c.y||0)+((c.height||0)-a)/2,width:b,height:a}}return c}pointAttribs(c,d){const f=p.prototype.pointAttribs.call(this,
c,d),e=this.options||{};var h=this.chart.options.plotOptions||{},g=h.series||{};const k=h.heatmap||{};h=c&&c.options.borderColor||e.borderColor||k.borderColor||g.borderColor;g=c&&c.options.borderWidth||e.borderWidth||k.borderWidth||g.borderWidth||f["stroke-width"];f.stroke=c&&c.marker&&c.marker.lineColor||e.marker&&e.marker.lineColor||h||this.color;f["stroke-width"]=g;d&&"normal"!==d&&(c=a(e.states&&e.states[d],e.marker&&e.marker.states&&e.marker.states[d],c&&c.options.states&&c.options.states[d]||
{}),f.fill=c.color||b.parse(f.fill).brighten(c.brightness||0).get(),f.stroke=c.lineColor||f.stroke);return f}translate(){const {borderRadius:b,marker:d}=this.options,f=d&&d.symbol||"rect",g=t[f]?f:"rect",k=-1!==["circle","square"].indexOf(g);this.generatePoints();this.points.forEach(function(d){const e=d.getCellAttributes();let h=Math.min(e.x1,e.x2);var l=Math.min(e.y1,e.y2);let n=Math.max(Math.abs(e.x2-e.x1),0),m=Math.max(Math.abs(e.y2-e.y1),0);d.hasImage=0===(d.marker&&d.marker.symbol||f||"").indexOf("url");
k&&(l=Math.abs(n-m),h=Math.min(e.x1,e.x2)+(n<m?0:l/2),l=Math.min(e.y1,e.y2)+(n<m?l/2:0),n=m=Math.min(n,m));d.hasImage&&(d.marker={width:n,height:m});d.plotX=d.clientX=(e.x1+e.x2)/2;d.plotY=(e.y1+e.y2)/2;d.shapeType="path";d.shapeArgs=a(!0,{x:h,y:l,width:n,height:m},{d:t[g](h,l,n,m,{r:c(b)?b:0})})});q(this,"afterTranslate")}}C.defaultOptions=a(x.defaultOptions,{animation:!1,borderRadius:0,borderWidth:0,interpolation:!1,nullColor:"#f7f7f7",dataLabels:{formatter:function(){const {numberFormatter:a}=
this.series.chart,{value:b}=this.point;return c(b)?a(b,-1):""},inside:!0,verticalAlign:"middle",crop:!1,overflow:"allow",padding:0},marker:{symbol:"rect",radius:0,lineColor:void 0,states:{hover:{lineWidthPlus:0},select:{}}},clip:!0,pointRange:null,tooltip:{pointFormat:"{point.x}, {point.y}: {point.value}<br/>"},states:{hover:{halo:!1,brightness:.2}},legendSymbol:"rectangle"});r(C.prototype,{axisTypes:k.seriesMembers.axisTypes,colorKey:k.seriesMembers.colorKey,directTouch:!0,getExtremesFromAll:!0,
parallelArrays:k.seriesMembers.parallelArrays,pointArrayMap:["y","value"],pointClass:D,specialGroup:"group",trackerGroups:k.seriesMembers.trackerGroups,alignDataLabel:n.prototype.alignDataLabel,colorAttribs:k.seriesMembers.colorAttribs,getSymbol:p.prototype.getSymbol});k.compose(C);v.registerSeriesType("heatmap",C);"";"";return C});u(b,"masters/modules/heatmap.src.js",[b["Core/Globals.js"],b["Core/Axis/Color/ColorAxis.js"]],function(b,k){b.ColorAxis=k;k.compose(b.Chart,b.Fx,b.Legend,b.Series)})});
//# sourceMappingURL=heatmap.js.map