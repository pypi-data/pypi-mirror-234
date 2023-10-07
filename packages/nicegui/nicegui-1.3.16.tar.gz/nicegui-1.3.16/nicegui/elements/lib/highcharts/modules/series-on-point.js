/*
 Highcharts JS v11.1.0 (2023-06-05)

 Series on point module

 (c) 2010-2022 Highsoft AS
 Author: Rafal Sebestjanski and Piotr Madej

 License: www.highcharts.com/license
*/
'use strict';(function(a){"object"===typeof module&&module.exports?(a["default"]=a,module.exports=a):"function"===typeof define&&define.amd?define("highcharts/modules/series-on-point",["highcharts"],function(g){a(g);a.Highcharts=g;return a}):a("undefined"!==typeof Highcharts?Highcharts:void 0)})(function(a){function g(a,d,c,g){a.hasOwnProperty(d)||(a[d]=g.apply(null,c),"function"===typeof CustomEvent&&window.dispatchEvent(new CustomEvent("HighchartsModuleLoaded",{detail:{path:d,module:a[d]}})))}var c=
a?a._modules:{};g(c,"Series/SeriesOnPointComposition.js",[c["Core/Series/Point.js"],c["Core/Series/Series.js"],c["Core/Series/SeriesRegistry.js"],c["Core/Renderer/SVG/SVGRenderer.js"],c["Core/Utilities.js"]],function(a,d,c,g,n){const {bubble:m,pie:r}=c.seriesTypes,{addEvent:h,defined:k,find:t,isNumber:u}=n;var l;(function(c){const l=[];c.compose=function(q,b){const {chartGetZData:e,seriesAfterInit:f,seriesAfterRender:a,seriesGetCenter:c,seriesShowOrHide:g,seriesTranslate:k}=p.prototype;r.prototype.onPointSupported=
!0;n.pushUnique(l,q)&&(h(d,"afterInit",f),h(d,"afterRender",a),h(d,"afterGetCenter",c),h(d,"hide",g),h(d,"show",g),h(d,"translate",k));n.pushUnique(l,b)&&(h(b,"beforeRender",e),h(b,"beforeRedraw",e));return q};class p{constructor(a){this.getRadii=m.prototype.getRadii;this.getRadius=m.prototype.getRadius;this.getPxExtremes=m.prototype.getPxExtremes;this.getZExtremes=m.prototype.getZExtremes;this.chart=a.chart;this.series=a;this.options=a.options.onPoint}drawConnector(){this.connector||(this.connector=
this.series.chart.renderer.path().addClass("highcharts-connector-seriesonpoint").attr({zIndex:-1}).add(this.series.markerGroup));const a=this.getConnectorAttributes();a&&this.connector.animate(a)}getConnectorAttributes(){const c=this.series.chart;var b=this.options;if(b){var e=b.connectorOptions||{},f=b.position,d=c.get(b.id);if(d instanceof a&&f&&k(d.plotX)&&k(d.plotY)){b=k(f.x)?f.x:d.plotX;var h=k(f.y)?f.y:d.plotY,l=e.width||1;d=e.stroke||this.series.color;e=e.dashstyle;f={d:g.prototype.crispLine([["M",
b,h],["L",b+(f.offsetX||0),h+(f.offsetY||0)]],l,"ceil"),"stroke-width":l};c.styledMode||(f.stroke=d,f.dashstyle=e);return f}}}seriesAfterInit(){this.onPointSupported&&this.options.onPoint&&(this.useMapGeometry=this.bubblePadding=!0,this.onPoint=new p(this))}seriesAfterRender(){delete this.chart.bubbleZExtremes;this.onPoint&&this.onPoint.drawConnector()}seriesGetCenter(c){var b=this.options.onPoint;const e=c.positions;if(b){const c=this.chart.get(b.id);c instanceof a&&k(c.plotX)&&k(c.plotY)&&(e[0]=
c.plotX,e[1]=c.plotY);if(b=b.position)k(b.x)&&(e[0]=b.x),k(b.y)&&(e[1]=b.y),b.offsetX&&(e[0]+=b.offsetX),b.offsetY&&(e[1]+=b.offsetY)}b=this.radii&&this.radii[this.index];u(b)&&(e[2]=2*b);c.positions=e}seriesShowOrHide(){const c=this.chart.series;this.points.forEach(b=>{const a=t(c,a=>(a=((a.onPoint||{}).options||{}).id)?a===b.id:!1);a&&a.setVisible(!a.visible,!1)})}seriesTranslate(){this.onPoint&&(this.onPoint.getRadii(),this.radii=this.onPoint.radii)}chartGetZData(){const a=[];this.series.forEach(b=>
{b=b.options.onPoint;a.push(b&&b.z?b.z:null)});this.series.forEach(b=>{b.onPoint&&(b.onPoint.zData=b.zData=a)})}}c.Additions=p})(l||(l={}));"";return l});g(c,"masters/modules/series-on-point.src.js",[c["Series/SeriesOnPointComposition.js"]],function(c){c.compose(a.Series,a.Chart)})});
//# sourceMappingURL=series-on-point.js.map