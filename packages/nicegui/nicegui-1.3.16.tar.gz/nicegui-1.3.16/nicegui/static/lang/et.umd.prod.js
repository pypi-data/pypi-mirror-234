/*!
 * Quasar Framework v2.12.2
 * (c) 2015-present Razvan Stoenescu
 * Released under the MIT License.
 */
(function(e,a){"object"===typeof exports&&"undefined"!==typeof module?module.exports=a():"function"===typeof define&&define.amd?define(a):(e="undefined"!==typeof globalThis?globalThis:e||self,e.Quasar=e.Quasar||{},e.Quasar.lang=e.Quasar.lang||{},e.Quasar.lang.et=a())})(this,function(){"use strict";var e={isoName:"et",nativeName:"Eesti",label:{clear:"Tühjenda",ok:"OK",cancel:"Tühista",close:"Sulge",set:"Määra",select:"Vali",reset:"Lähtesta",remove:"Eemalda",update:"Uuenda",create:"Loo",search:"Otsi",filter:"Filtreeri",refresh:"Värskenda",expand:e=>e?`Laienda "${e}"`:"Laienda",collapse:e=>e?`Ahenda "${e}"`:"Ahenda"},date:{days:"pühapäev_esmaspäev_teisipäev_kolmapäev_neljapäev_reede_laupäev".split("_"),daysShort:"P_E_T_K_N_R_L".split("_"),months:"jaanuar_veebruar_märts_aprill_mai_juuni_juuli_august_september_oktoober_november_detsember".split("_"),monthsShort:"jaan_veebr_märts_apr_mai_juuni_juuli_aug_sept_okt_nov_dets".split("_"),firstDayOfWeek:1,format24h:!0,pluralDay:"päeva"},table:{noData:"Andmeid ei ole",noResults:"Sobivaid kirjeid ei leitud",loading:"Laadimine...",selectedRecords:e=>1===e?"1 kirje valitud.":e+" kirjet valitud.",recordsPerPage:"Kirjed lehel:",allRows:"Kõik",pagination:(e,a,i)=>e+"-"+a+" / "+i,columns:"Veerud"},editor:{url:"URL",bold:"Rasvane",italic:"Kaldkiri",strikethrough:"Läbikriipsutatud",underline:"Allakriipsutatud",unorderedList:"Järjestamata loend",orderedList:"Järjestatud loend",subscript:"Alaindeks",superscript:"Ülaindeks",hyperlink:"Link",toggleFullscreen:"Täisekraan",quote:"Tsitaat",left:"Joonda vasakule",center:"Joonda keskele",right:"Joonda paremale",justify:"Joonda võrdselt",print:"Prindi",outdent:"Vähenda taanet",indent:"Suurenda taanet",removeFormat:"Eemalda vormindus",formatting:"Vormindamine",fontSize:"Fondi suurus",align:"Joonda",hr:"Horisontaalne joon",undo:"Võta tagasi",redo:"Tee uuesti",heading1:"Pealkiri 1",heading2:"Pealkiri 2",heading3:"Pealkiri 3",heading4:"Pealkiri 4",heading5:"Pealkiri 5",heading6:"Pealkiri 6",paragraph:"Lõik",code:"Kood",size1:"Väga väike",size2:"Natuke väike",size3:"Normaalne",size4:"Keskmiselt suur",size5:"Suur",size6:"Väga suur",size7:"Maksimaalne",defaultFont:"Vaikefont",viewSource:"Kuva allikas"},tree:{noNodes:"Ühtegi sõlme pole saadaval",noResults:"Sobivaid sõlmi ei leitud"}};return e});