/*jshint esversion: 6 */
/**
 * This function is used to get cookie so that csrf token can be set while sending request to backend
 * @param {string} name - Name to get cookie by name
 * @returns {string} cookieValue - Value of cookie corresponding to name
 */
function getCookie(name) {  
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        let cookies = document.cookie.split(";");
        
        (function() {
            let i = 0;
            for ( i = 0; i < cookies.length; i+=1) {
                let cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        })();        
    }
    return cookieValue;
}

/**
 * This function is used to send XML request to backend
 * It uses Promises to send asynchronus requests 
 * @param {string} url - url defined in urls.py to which request must be made
 * @param {string} type - type of request {'POST' / 'GET'}
 * @param {object} data - data to be sent to backend in case of POST request
 */

function sendRequest(url,type,data){
    let request = new XMLHttpRequest();
    let csrftoken = getCookie("csrftoken");
    return new Promise(function(resolve, reject){
        request.onreadystatechange = () => {
            if (request.readyState !== 4) return;
            // Process the response
			if (request.status >= 200 && request.status < 300) {
                // If successful
				resolve(request.responseText);
			} else {
				// If failed
				reject({
					status: request.status,
					statusText: request.statusText
				});
			}
        };
        // Setup our HTTP request
		request.open(type || "GET", url, true);
        // Add csrf token
        request.setRequestHeader("X-CSRFToken", csrftoken);
        // Send the request
        request.send(JSON.stringify(data));
    });
    
}

/**
 * 
 * @param {object} latlng - dictionary corresponding to latitude longitude of location clicked
 */

function latlonToBackend(latlng){
    console.log(latlng.lat);
    console.log(latlng.lng);

    sendRequest("/myapp/getUTM/","POST",latlng)
	.then(function (response) {
        console.log("Success!",response);
            response = JSON.parse(response);
            let Arr3d={
                "red": response.red,
                "blue": response.blue,
                "green": response.green,
                "nir": response.nir,
                "swir1": response.swir1,
                "swir2": response.swir2,

            };
            let Arr1d = {
                "red":[],
                "blue":[],
                "green":[],
                "nir":[],
                "swir1":[],
                "swir2":[]
            };
            console.log(Arr3d);
            for(let band in Arr3d){ //band contains keys of Arr3d dictionary
                if(Arr3d.hasOwnProperty(band)){ //hasOwnProperty should be used while using for in loop... It is useful if there are undesired enumerable properties in the object prototype. This might be the case if you e.g. use certain JavaScript libraries.
                    for(let i=0; i<Arr3d[band].length; i+=1){
                        for(let j=0; j<Arr3d[band][i].length; j+=1){
                            Arr1d[band] = Arr1d[band].concat(Arr3d[band][i][j]);
                        }
                    }
                }
            }
            console.log(Arr1d);
            let time = response.time;
            console.log(time);
            drawGraph(Arr1d,time);
        })        
	.catch(function (error) {
		console.log("Something went wrong", error);
    });
}


// initialize the map 
let map = L.map("map").setView([29.380304, 79.463570],10);
let MyBingMapsKey = "ApDp98sLLH6Lggj-ExrPosLg8IDo0exkQYMu6qU41XgOMheh1NDWyd1HHzyVbny9";
let bingLayer = L.bingLayer(MyBingMapsKey);
let osmLayer = new L.TileLayer("http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png");

let baseLayers = {
    "bingLayer":bingLayer,
    "osmLayer":osmLayer
};
L.control.layers(baseLayers).addTo(map);

let searchControl = new L.esri.Controls.Geosearch().addTo(map);

let results = new L.LayerGroup().addTo(map);

searchControl.on("results", function(data){
    results.clearLayers();
    for (let i = data.results.length - 1; i >= 0; i--) {
      results.addLayer(L.marker(data.results[i].latlng));
    }
});


map.pm.addControls({
    position: "topleft",
    drawCircle: false,
  });

map.on("click", function(e){
 let coord = e.latlng;
 let lat = coord.lat;
 let lng = coord.lng;
 console.log("You clicked the map at latitude: " + lat + " and longitude: " + lng);
 if(document.getElementById("selectIndex").value != "terrainProfile"){
     document.getElementById("loader").style.display = "block";
    latlonToBackend(coord);
 }
}); 

currentShapeLatLngs = [];

// listen to vertexes being added to currently drawn layer (called workingLayer)
map.on("pm:drawstart", ({ workingLayer }) => {
    currentShapeLatLngs = workingLayer._latlngs;
});

map.on("pm:drawend", (e) => {
    console.log(currentShapeLatLngs);
    if(document.getElementById("selectIndex").value === "terrainProfile"){
        document.getElementById("loader").style.display="block";
        sendRequest("/myapp/getElevations/","POST",{"latLngArray":currentShapeLatLngs}).then((e)=>{
            distElevationArray  = JSON.parse(e).elevationProfile;
            yArr = [];
            xArr = [];
            for(let i of distElevationArray){
                console.log(i);
                xArr.push(i.distance);
                yArr.push(i.elevation);
            }
            console.log(xArr);
            console.log(yArr);
            TESTER = document.getElementById("tester");
            let layout = {
                title: {
                  text:"Elevation Profile",
                  font: {
                    family: "Courier New, monospace",
                    size: 24
                  },
                  xref: "paper",
                  x: 0.05,
                },
                xaxis: {
                  title: {
                    text: "Distance (in km)",
                    font: {
                      family: "Courier New, monospace",
                      size: 18,
                      color: "#7f7f7f"
                    }
                  },
                },
                yaxis: {
                  title: {
                    text: "Elevation (in meters)",
                    font: {
                      family: "Courier New, monospace",
                      size: 18,
                      color: "#7f7f7f"
                    }
                  }
                }
              };
                Plotly.purge(TESTER);
                Plotly.plot( TESTER, [{
                y: yArr,
                x: xArr,
                }], layout );
            console.log(distElevationArray);
            document.getElementById("loader").style.display="none";
        }).catch(
            (e)=>{
                console.log("Error ",e);
                alert("Some Error occured... Please try again in a while");
                document.getElementById("loader").style.display="none";
            }
        );
    }
});

function drawGraph(Arr1d,timeArr){
    let e = document.getElementById("selectIndex");
    let indexName = e.options[e.selectedIndex].text;
    let url = "/myapp/getIndexFormula/";
    let data = {"indexName":indexName};
    sendRequest(url,"POST",data)
    .then(function (response) {
            response = JSON.parse(response);
            console.log(response);
            indexName = response.index.indexName;
            indexFormula = response.index.indexFormula;
            console.log(indexFormula);
            xArr = [];
            for(let i=0; i<Arr1d.red.length; i+=1){
                r = Arr1d.red[i];
                g = Arr1d.green[i];
                b = Arr1d.blue[i];
                nir = Arr1d.nir[i];
                swir1 = Arr1d.swir1[i];
                swir2 = Arr1d.swir2[i];
                ans = math.compile(indexFormula).eval({
                    "r":r,
                    "g":g,
                    "b":b,
                    "nir":nir,
                    "swir1":swir1,
                    "swir2":swir2
                });
                console.log("[r,g,b,nir,swir1,swir2] = ",[r,g,b,nir,swir1,swir2]);
                if(isNaN(ans)){
                    console.log("shit");
                    timeArr.splice(i,1);
                    continue;
                }
                console.log("[eval result] = ",ans);
                xArr.push(ans);
            }
            console.log("xArr is : ",xArr);
            let e = document.getElementById("selectIndex");
            let layout = {
                title: {
                  text:"Index Plot",
                  font: {
                    family: "Courier New, monospace",
                    size: 24
                  },
                  xref: "paper",
                  x: 0.05,
                },
                xaxis: {
                  title: {
                    text: "Time",
                    font: {
                      family: "Courier New, monospace",
                      size: 18,
                      color: "#7f7f7f"
                    }
                  },
                },
                yaxis: {
                  title: {
                    text: "Value",
                    font: {
                      family: "Courier New, monospace",
                      size: 18,
                      color: "#7f7f7f"
                    }
                  }
                }
              };
            TESTER = document.getElementById("tester");
                Plotly.purge(TESTER);
                Plotly.plot( TESTER, [{
                y: xArr,
                x: timeArr,
                name: e.options[e.selectedIndex].text}],layout);
            document.getElementById("loader").style.display="none";
        })
    .catch(function (error) {
		console.log("Something went wrong", error);
    });
}

function saveIndex(index){
    console.log(index);
    let url = "/myapp/saveIndex/";
    sendRequest(url,"POST",index).then(
        function (response) {
            getIndices();
        }
    ).catch(
        function (error) {
            console.log("Something went wrong", error);
        }
    );
}

function getIndices(){
    let url = "/myapp/getIndices";
    sendRequest(url,"GET").then(
        function (response) {
            response = JSON.parse(response);
            indicesNames =  response.indicesNames;
            indicesFormulas = response.indicesFormulas;
            console.log(indicesNames,indicesFormulas);
            indexDict = {};
            for(let i=0; i<indicesNames.length; i+=1){
                a = indicesNames[i];
                b = indicesFormulas[i];
                indexDict[indicesNames[i]] = {
                    "name" : a,
                    "formula" : b
                };
            }
            console.log(indexDict);
            $("#selectIndex").empty();
            $.each(indexDict, function(key, value) {   
                $("#selectIndex")
                    .append($("<option></option>")
                               .attr("value",key)
                               .text(value.name+" : "+value.formula)); 
           });
           $("#selectIndex").append("<option value='terrainProfile'>Draw Terrain Profile</option>");
           $("#selectIndex").append("<option value='other'>Add your own index</option>");
           document.getElementById("indexInputField").style.display = "none";
           document.getElementById("map").style.display = "block";
           document.getElementById("tester").style.display = "block";
        }
    ).catch(
        function (error) {
            console.log("Something went wrong", error);
        }
    );
}