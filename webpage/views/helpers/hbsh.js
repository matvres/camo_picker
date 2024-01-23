const hbs = require('hbs');

hbs.registerHelper("generateBarchart",()=>{

    return "TEST DELA";
})

hbs.registerHelper("nameToCountry",(name)=>{
    if (name){
        var split = name.split("/");
        if (split.length > 4) {
            return split[3].replace("_", " ");
        } else {
            return "Nepoznano";
        }
    } else {
        return "Nepoznano";
    }
})

hbs.registerHelper("checkLength",(val)=>{
    if (val.length > 0){
        return "yes";
    } else {
        return null;
    }
})

hbs.registerHelper("returnPercentage",(val)=>{
    return (val * 100).toFixed(2);
})

hbs.registerHelper("returnPercentageToDraw",(val)=>{
    return Math.round(val * 100 * 0.95);
})

hbs.registerHelper("checkFamily",(val)=>{
    if (val.length > 0){
        return "<span><b>Družina: </b>" + val + "</span>";
    } else {
        return "<p>&nbsp</p>";
    }
})
