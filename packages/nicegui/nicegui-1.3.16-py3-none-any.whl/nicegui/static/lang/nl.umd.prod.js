/*!
 * Quasar Framework v2.12.2
 * (c) 2015-present Razvan Stoenescu
 * Released under the MIT License.
 */
(function(e,n){"object"===typeof exports&&"undefined"!==typeof module?module.exports=n():"function"===typeof define&&define.amd?define(n):(e="undefined"!==typeof globalThis?globalThis:e||self,e.Quasar=e.Quasar||{},e.Quasar.lang=e.Quasar.lang||{},e.Quasar.lang.nl=n())})(this,function(){"use strict";var e={isoName:"nl",nativeName:"Nederlands",label:{clear:"Wis",ok:"OK",cancel:"Annuleer",close:"Sluit",set:"Pas toe",select:"Selecteer",reset:"Herinitialiseren",remove:"Verwijder",update:"Update",create:"Maak aan",search:"Zoek",filter:"Filter",refresh:"Ververs",expand:e=>e?`"${e}" uitklappen`:"Uitklappen",collapse:e=>e?`"${e}" inklappen`:"Inklappen"},date:{days:"Zondag_Maandag_Dinsdag_Woensdag_Donderdag_Vrijdag_Zaterdag".split("_"),daysShort:"Zo_Ma_Di_Wo_Do_Vr_Za".split("_"),months:"Januari_Februari_Maart_April_Mei_Juni_Juli_Augustus_September_Oktober_November_December".split("_"),monthsShort:"Jan_Feb_Mrt_Apr_Mei_Jun_Jul_Aug_Sep_Okt_Nov_Dec".split("_"),firstDayOfWeek:1,format24h:!0,pluralDay:"dagen"},table:{noData:"Geen gegevens beschikbaar",noResults:"Geen records gevonden",loading:"Laden...",selectedRecords:e=>1===e?"1 record geselecteerd.":(0===e?"Geen":e)+" geselecteerde records.",recordsPerPage:"Records per pagina:",allRows:"Alle",pagination:(e,n,r)=>e+"-"+n+" van "+r,columns:"Kolommen"},editor:{url:"URL",bold:"Vet",italic:"Cursief",strikethrough:"Doorstrepen",underline:"Onderstrepen",unorderedList:"Ongeordende lijst",orderedList:"Geordende lijst ",subscript:"Onderschrift",superscript:"Bovenschrift",hyperlink:"Hyperlink",toggleFullscreen:"Volledig scherm",quote:"Citaat",left:"Links uitlijnen",center:"Centreren",right:"Rechts uitlijnen",justify:"Uitvullen",print:"Afdrukken",outdent:"Minder inspringen",indent:"Meer inspringen",removeFormat:"Opmaak verwijderen",formatting:"Opmaak",fontSize:"Tekengrootte",align:"Uitlijnen",hr:"Horizontale lijn invoegen",undo:"Herstel",redo:"Opnieuw",heading1:"Kop 1",heading2:"Kop 2",heading3:"Kop 3",heading4:"Kop 4",heading5:"Kop 5",heading6:"Kop 6",paragraph:"Paragraaf",code:"Code",size1:"Heel klein",size2:"Klein",size3:"Normaal",size4:"Medium",size5:"Groot",size6:"Heel groot",size7:"Maximum",defaultFont:"Standaard lettertype",viewSource:"Bekijk bron"},tree:{noNodes:"Geen nodes beschikbaar",noResults:"Geen overeenkomstige nodes gevonden"}};return e});