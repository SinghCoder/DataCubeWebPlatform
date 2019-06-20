/*jshint esversion: 6 */
/**
 * This function is used to get cookie so that csrf token can be set while sending request to backend
 * Already avaiable on net, just copy paste
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
 * This function is what plots the graph using plotly js
 * @param {string} graphTitle 
 * @param {string} xTitle 
 * @param {string} yTitle 
 * @param {Array} xArr 
 * @param {Array} yArr 
 * @param {string} plotName 
 * @param {boolean} multipleAllowed - whether or not multiple plots allowed on one graph
 */
function plotGraph(graphTitle,xTitle,yTitle,xArr,yArr,plotName,multipleAllowed = false){
    let e = document.getElementById("selectIndex");
            let layout = {
                title: {
                  text:graphTitle,
                  font: {
                    family: "Courier New, monospace",size: 24
                  }
                },
                xaxis: {
                  title: {
                    text: xTitle,
                    font: {
                      family: "Courier New, monospace",size: 18,color: "#7f7f7f"
                    }
                  },
                },
                yaxis: {
                  title: {
                    text: yTitle,
                    font: {
                      family: "Courier New, monospace",size: 18,color: "#7f7f7f"
                    }
                  }
                }
              };
            TESTER = document.getElementById("tester");
                // Plotly.purge(TESTER);
                let plottingFunction = (multipleAllowed == true) ? 'plot' : 'newPlot';
                Plotly[plottingFunction]( TESTER, [{
                x: xArr,
                y: yArr,
                name : plotName}],layout);            
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
 * This function is called whenever user clicks on map at a location
 * It retrieves latitude and longitude values from leaflet and sends to backend
 * Backend inturn sends back time series pixel values of all available bands as
 * a dictionary of 3d arrays for that location.
 * This is inturn passed to plotly.js to plot graph of index user has currently selected in drop down list
 * @param {object} latlng - dictionary corresponding to latitude longitude of location clicked
 */

function latlonToBackend(latlng){
    // console.log(latlng.lat);
    // console.log(latlng.lng);
    sendRequest("/myapp/getUTM/","POST",latlng)
	.then(function (response) {
        response = JSON.parse(response);
        console.log(response['error']);
        if(response['error'] == 'Empty Dataset'){
            // console.log('oyeeeeeeeeee');
            document.getElementById("loader").style.display="none";
            swal("Error", "Data not available for this point! Try another point..", "error");
            return;
        }
        console.log("Success!",response);
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
            // console.log(Arr1d);
            let time = response.time;   //time's 1d array
            // console.log(time);
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
        sendRequest("/myapp/getElevations/","POST",{"latLngArray":currentShapeLatLngs}).then((res)=>{
            res = JSON.parse(res);
            if(res['error'] == 'Empty Dataset'){
                // console.log('oyeeeeeeeeee');
                document.getElementById("loader").style.display="none";
                swal("Error", "Data not available for these ranges! Try some other region..", "error");
                return;
            }
            distElevationArray  = res.elevationProfile;
            y1Arr = [];
            y2Arr = [];
            xArr = [];
            for(let i of distElevationArray){
                console.log(i);
                xArr.push(i.distance);
                y1Arr.push(i.elevation.srtm);
                y2Arr.push(i.elevation.aster)
            }
            console.log(xArr);
            console.log(y1Arr);
            console.log(y2Arr);
            plotGraph('Elevation Profile','Distance (in Kms)','Height(in meters)',xArr,y1Arr,'srtm',false);
            plotGraph('Elevation Profile','Distance (in Kms)','Height(in meters)',xArr,y2Arr,'aster',true);
            // console.log(distElevationArray);
            document.getElementById("loader").style.display="none";
            swal("Success", "Elevation Profile is drawn... Click Slide Out to see the graph", "success");
        }).catch(
            (e)=>{
                console.log("Error ",e);
                alert("Some Error occured... Please try again in a while");
                document.getElementById("loader").style.display="none";
            }
        );
    }
});

/**
 * This function takes input pixel values time series data for all years corresponding to that location and 
 * process the indexFormula corresponding to selected Index using Math.js math.compile()
 * and .eval() function, compile() compiles formula and eval() evaluates it.It then passes these values to plotly js to plot
 * a graph
 * @param {Object} Arr1d - dictionary containing 1d arrays of pixel values for all the bands
 * @param {Array<string>} timeArr - 1d array containing time values as strings in format {YYYY-MM-DD}
 */

function drawGraph(Arr1d,timeArr){
    let e = document.getElementById("selectIndex");
    let indexName = e.options[e.selectedIndex].text;
    let url = "/myapp/getIndexFormula/";
    let data = {"indexName":indexName};
    sendRequest(url,"POST",data)
    .then(function (response) {
            response = JSON.parse(response);
            // console.log(response);
            indexName = response.index.indexName;
            indexFormula = response.index.indexFormula;
            // console.log(indexFormula);
            yArr = [];
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
                    timeArr.splice(i,1);
                    continue;
                }
                console.log("[eval result] = ",ans);
                yArr.push(ans);
            }
            // console.log("xArr is : ",xArr);
            plotGraph(indexName+' Plot','Time','indexValue',timeArr,yArr,indexName,false);
            document.getElementById("loader").style.display="none";
            swal("Success", "Graph is drawn... Click Slide Out to see the graph", "success");
        })
    .catch(function (error) {
        console.log("Something went wrong", error);
        document.getElementById("loader").style.display="none";
        swal("Error", "Got an error"+e, "error");
    });
}

/**
 * This function is called when user clicks on GO button on calculator while adding his/her own 
 * customized index. It takes index name and formula and sends a request to backend to save it in 
 * his user account.
 * @param {string} index - index name and formula to be saved in database
 */

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

/**
 * This function is used to query about indices available in particular user's account
 * Takes from backend all indices available and populate the select field at top right of webpage
 */

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
        //    document.getElementById("tester").style.display = "block";
        }
    ).catch(
        function (error) {
            console.log("Something went wrong", error);
        }
    );
}

