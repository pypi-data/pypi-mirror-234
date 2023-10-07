/*
 Highcharts JS v11.1.0 (2023-06-05)

 Support for parallel coordinates in Highcharts

 (c) 2010-2021 Pawel Fus

 License: www.highcharts.com/license
*/
'use strict';(function(b){"object"===typeof module&&module.exports?(b["default"]=b,module.exports=b):"function"===typeof define&&define.amd?define("highcharts/modules/parallel-coordinates",["highcharts"],function(d){b(d);b.Highcharts=d;return b}):b("undefined"!==typeof Highcharts?Highcharts:void 0)})(function(b){function d(b,k,d,p){b.hasOwnProperty(k)||(b[k]=p.apply(null,d),"function"===typeof CustomEvent&&window.dispatchEvent(new CustomEvent("HighchartsModuleLoaded",{detail:{path:k,module:b[k]}})))}
b=b?b._modules:{};d(b,"Extensions/ParallelCoordinates.js",[b["Core/Axis/Axis.js"],b["Core/Chart/Chart.js"],b["Core/Templating.js"],b["Core/Globals.js"],b["Core/Defaults.js"],b["Core/Series/Series.js"],b["Core/Utilities.js"]],function(b,k,d,p,z,q,r){function A(a){var f=this.series&&this.series.chart;let b=a.apply(this,Array.prototype.slice.call(arguments,1)),e,g,c;f&&f.hasParallelCoordinates&&!t(b.formattedValue)&&(c=f.yAxis[this.x],e=c.options,f=(g=w(e.tooltipValueFormat,e.labels.format))?B(g,x(this,
{value:this.y}),f):c.dateTime?f.time.dateFormat(f.time.resolveDTLFormat(e.dateTimeLabelFormats[c.tickPositions.info.unitName]).main,this.y):e.categories?e.categories[this.y]:this.y,b.formattedValue=b.point.formattedValue=f);return b}const {format:B}=d;({setOptions:d}=z);const {addEvent:l,arrayMax:C,arrayMin:D,defined:t,erase:E,extend:x,insertItem:F,isNumber:u,merge:m,pick:w,splat:v,wrap:G}=r;r=k.prototype;const y={lineWidth:0,tickLength:0,opposite:!0,type:"category"};d({chart:{parallelCoordinates:!1,
parallelAxes:{lineWidth:1,title:{text:"",reserveSpace:!1},labels:{x:0,y:4,align:"center",reserveSpace:!1},offset:0}}});l(k,"init",function(a){a=a.args[0];const f=v(a.yAxis||{}),b=[];let e=f.length;if(this.hasParallelCoordinates=a.chart&&a.chart.parallelCoordinates){for(this.setParallelInfo(a);e<=this.parallelInfo.counter;e++)b.push({});a.legend||(a.legend={});"undefined"===typeof a.legend.enabled&&(a.legend.enabled=!1);m(!0,a,{boost:{seriesThreshold:Number.MAX_VALUE},plotOptions:{series:{boostThreshold:Number.MAX_VALUE}}});
a.yAxis=f.concat(b);a.xAxis=m(y,v(a.xAxis||{})[0])}});l(k,"update",function(a){a=a.options;a.chart&&(t(a.chart.parallelCoordinates)&&(this.hasParallelCoordinates=a.chart.parallelCoordinates),this.options.chart.parallelAxes=m(this.options.chart.parallelAxes,a.chart.parallelAxes));this.hasParallelCoordinates&&(a.series&&this.setParallelInfo(a),this.yAxis.forEach(function(a){a.update({},!1)}))});x(r,{setParallelInfo:function(a){const b=this;a=a.series;b.parallelInfo={counter:0};a.forEach(function(a){a.data&&
(b.parallelInfo.counter=Math.max(b.parallelInfo.counter,a.data.length-1))})}});l(q,"bindAxes",function(a){if(this.chart.hasParallelCoordinates){const b=this;this.chart.axes.forEach(a=>{F(b,a.series);a.isDirty=!0});b.xAxis=this.chart.xAxis[0];b.yAxis=this.chart.yAxis[0];a.preventDefault()}});l(q,"afterTranslate",function(){let a=this.chart,b=this.points,d=b&&b.length,e=Number.MAX_VALUE,g,c,h;if(this.chart.hasParallelCoordinates){for(h=0;h<d;h++)c=b[h],t(c.y)?(c.plotX=a.polar?a.yAxis[h].angleRad||0:
a.inverted?a.plotHeight-a.yAxis[h].top+a.plotTop:a.yAxis[h].left-a.plotLeft,c.clientX=c.plotX,c.plotY=a.yAxis[h].translate(c.y,!1,!0,void 0,!0),u(c.high)&&(c.plotHigh=a.yAxis[h].translate(c.high,!1,!0,void 0,!0)),"undefined"!==typeof g&&(e=Math.min(e,Math.abs(c.plotX-g))),g=c.plotX,c.isInside=a.isInsidePlot(c.plotX,c.plotY,{inverted:a.inverted})):c.isNull=!0;this.closestPointRangePx=e}},{order:1});l(q,"destroy",function(){this.chart.hasParallelCoordinates&&(this.chart.axes||[]).forEach(function(a){a&&
a.series&&(E(a.series,this),a.isDirty=a.forceRedraw=!0)},this)});["line","spline"].forEach(function(a){G(p.seriesTypes[a].prototype.pointClass.prototype,"getLabelConfig",A)});class H{constructor(a){this.axis=a}setPosition(a,b){const d=this.axis,e=d.chart,g=((this.position||0)+.5)/(e.parallelInfo.counter+1);e.polar?b.angle=360*g:(b[a[0]]=100*g+"%",d[a[1]]=b[a[1]]=0,d[a[2]]=b[a[2]]=null,d[a[3]]=b[a[3]]=null)}}var n;(function(a){function b(a){const b=this.chart,d=this.parallelCoordinates;let e=["left",
"width","height","top"];if(b.hasParallelCoordinates)if(b.inverted&&(e=e.reverse()),this.isXAxis)this.options=m(this.options,y,a.userOptions);else{const c=b.yAxis.indexOf(this);this.options=m(this.options,this.chart.options.chart.parallelAxes,a.userOptions);d.position=w(d.position,0<=c?c:b.yAxis.length);d.setPosition(e,this.options)}}function d(a){const b=this.chart,d=this.parallelCoordinates;if(d&&b&&b.hasParallelCoordinates&&!this.isXAxis){const b=d.position;let c=[];this.series.forEach(function(a){a.yData&&
a.visible&&u(b)&&c.push.apply(c,v(a.yData[b]))});c=c.filter(u);this.dataMin=D(c);this.dataMax=C(c);a.preventDefault()}}function e(){this.parallelCoordinates||(this.parallelCoordinates=new H(this))}a.compose=function(a){a.keepProps.push("parallel");l(a,"init",e);l(a,"afterSetOptions",b);l(a,"getSeriesExtremes",d)}})(n||(n={}));n.compose(b);return n});d(b,"masters/modules/parallel-coordinates.src.js",[],function(){})});
//# sourceMappingURL=parallel-coordinates.js.map