const fs = require('fs')

const os = require('os')

const {spawn} = require('child_process')

const multer = require('multer')
const { win32 } = require('path')

var storage = multer.diskStorage({
    destination: function (req, file, callback) {
        callback(null, './public/images')
    },
    filename: function (req, file, callback) {
        callback(null, generateFileName(file.originalname))
    }
})

function generateFileName(originalName){
    var name = originalName.split('.');

    return name[0]+'-'+Date.now()+'.'+name[name.length - 1];
}

const fileFilter = function (req, file, callback) {
    if (file.mimetype === "image/jpeg" || file.mimetype === "image/png") {
        callback(null, true);
    } else {
        callback(new Error("Samo png in jpeg slike so veljavne."), false);
    }
}

var upload = multer({ storage: storage, limits: {fileSize: 1024 * 1024 * 5}, fileFilter: fileFilter}).single('image');

function getPercentage(counts, hexPictureColors) {
    var i;
    var totalCounts = 0;
    for (i = 0; i < counts.length; i++) {
        totalCounts += counts[i];
    }
    var percentage = new Array(counts.length);
    for (i = 0; i < counts.length; i++) {
        percentage[i] = counts[i] / totalCounts;
    }

    var temp;
    var colorPercentageArray = new Array(counts.length);
    for (i = 0; i < counts.length; i++) {
        temp = new Object();
        temp.color = hexPictureColors[i];
        temp.percentage = percentage[i];
        colorPercentageArray[i] = temp;
    }
    return colorPercentageArray;
}

function getBestCamos(allCamos, counts, pictureColors){

    var i;
    var totalCounts = 0;
    for (i = 0; i < counts.length; i++) {
        totalCounts += counts[i];
    }
    var percentage = new Array(counts.length);
    for (i = 0; i < counts.length; i++) {
        percentage[i] = counts[i] / totalCounts;
    }
    //console.log(percentage)


    var camo_marks = [];

    var curr_total = 9999;
    var temp;
    var temp_min;
    var temp_max;

    var r;
    var g;
    var b;

    //zanka cez vse kamoflaze
    var index_camo;
    var index_color_pic;
    var index_camo_color_compare;
    for (index_camo = 0; index_camo < allCamos.length; index_camo++) {

        curr_total = 0;

        //zanka cez vse barve slike
        for (index_color_pic = 0; index_color_pic < pictureColors.length; index_color_pic++) {

            temp_min = 999999;
            temp_max = 0;

            //zanka cez vse barve kamoflaze da se primerja z barvo slike
            for (index_camo_color_compare = 0; index_camo_color_compare < allCamos[index_camo].colors.length; index_camo_color_compare++) {

                //zracunaj diff
                r = Math.abs(pictureColors[index_color_pic][0] - allCamos[index_camo].colors[index_camo_color_compare].rgb[0]);
                g = Math.abs(pictureColors[index_color_pic][1] - allCamos[index_camo].colors[index_camo_color_compare].rgb[1]);
                b = Math.abs(pictureColors[index_color_pic][2] - allCamos[index_camo].colors[index_camo_color_compare].rgb[2]);
                temp = (r + g + b) * (Math.abs(percentage[index_color_pic] - allCamos[index_camo].colors[index_camo_color_compare].percentage));

                //update if smaller
                if (temp < temp_min) {
                    temp_min = temp;
                }
                if (temp > temp_max) {
                    temp_max = temp;
                }
            }
            //add current color mark to total colors mark
            curr_total += (percentage[index_color_pic] * temp_min);
        }
        //dodaj minimum diff v tabelo camo ocen
        camo_marks.push(curr_total)
    }

    //dodaj oceno + indeks kot key value pair v dictionary
    var dictionary_camo_marsk = {};
    for (i = 0; i < camo_marks.length; i++) {
        dictionary_camo_marsk[camo_marks[i]] = i;
    }
    //sort arr
    camo_marks.sort(function(a, b) {
        return a - b;
    });

    bestCamos = []
    for (i = 0; i < camo_marks.length; i++) {
        bestCamos.push(allCamos[dictionary_camo_marsk[camo_marks[i]]])
    }

    //console.log(camo_marks)


    var result = []
    result.push(bestCamos[0]);
    result.push(bestCamos[1]);
    result.push(bestCamos[2]);

    result.push(bestCamos[3]);
    result.push(bestCamos[4]);
    //result.push(bestCamos[5]);
    return result;
}

const upload_img = async (req, res) => {
    upload(req, res, function (err){

        //ce ni png ali jpeg
        if(err){
            return res.render('error', { title: 'CAMOPICKER', message: "Niste poslali slike, ampak neko drugo datoteko", error:{status: "napaka", stack: "napaka pri nalaganju slike"} });
        }
        //ce submita prazno brez datoteke
        if (!req.file || !req.file.path) {
            return res.render('error', { title: 'CAMOPICKER', message: "Slika ni bila poslana", error:{status: "napaka", stack: "napaka pri nalaganju slike"} });
        }

        var response = {
            image: req.file.path
        }

        
    
        var stringGetPath = req.file.path.substring(6, req.file.path.length)

        // TODO CALL Python Script
        if(os.platform() == "win32"){
            var py = 'python'
        }else{
            var py = 'python3'
        }

        

        var dataToSend; 
        const python = spawn(py,["../color_identifier.py",stringGetPath])
        python.stdout.on('data',(data) => {
            console.log("pipedata from python script")
            dataToSend = data.toString()
            console.log(dataToSend)

        });

        
        python.on('close',(code) => {
            console.log("skripta se je končala z",code)

            
            if(os.platform() == "win32"){
                var splt = stringGetPath.split('\\')
            }else{
                var splt = stringGetPath.split('/')
            }

            fs.readFile("./public/files/" + splt[splt.length-1] + "_graf.txt", "utf8", (err,data) => {
                if(err){
                    console.log(err)
                    return res.render('error', { title: 'CAMOPICKER', message: "napaka pri branju iz datoteke", error:{status: "napaka", stack: "napaka pri branju"} });
                }else{
                    graf = JSON.parse(data)

                    var oznaka = JSON.stringify(graf[0])
                    var podatki = JSON.stringify(graf[1])
                    //console.log(graf)
                    var digital = "/files/" + splt[splt.length-1]
                    var digital2 = "/files/" + "2" + splt[splt.length-1]
                    var digital3 = "/files/" + "3" + splt[splt.length-1]


                    var voro1 = "/files/" + "v1" + splt[splt.length-1]
                    var voro2 = "/files/" + "v2" + splt[splt.length-1]

                    var bestCamos =getBestCamos(req.app.locals.camo_json, graf[1], graf[2]);

                    var colorPercentageArray = getPercentage(graf[1], graf[0]);

                    res.render('generated', { title: 'CAMOPICKER', slika: stringGetPath, oznaka: oznaka, podatki: podatki, barve: graf[0], digital: digital, digital2: digital2, digital3: digital3, bestCamos: bestCamos, voro1: voro1, voro2: voro2, colorPercentageArray:colorPercentageArray});

                    //test camos.json
                    //console.log(req.app.locals.camo_json[0]);
                }
            });
            
            // return 
        });
        
        

        //res.redirect("/");

        //res.setHeader("Content-Type", "application/json");
        //res.end(JSON.stringify(response))
    });
}

module.exports = {
    upload_img
}
