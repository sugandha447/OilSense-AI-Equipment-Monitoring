/*=========================================
OilSense AI Dashboard
Professional JavaScript
==========================================*/

/*==============================
LOADER
==============================*/

window.addEventListener("load", function () {

    const loader = document.getElementById("loader");

    setTimeout(function () {

        loader.style.opacity = "0";

        loader.style.visibility = "hidden";

    }, 800);

});


/*==============================
LIVE DATE & TIME
==============================*/

function updateClock() {

    const now = new Date();

    const options = {

        weekday: "short",

        day: "numeric",

        month: "short",

        year: "numeric",

        hour: "2-digit",

        minute: "2-digit",

        second: "2-digit"

    };

    const clock = document.getElementById("liveDateTime");

    if(clock){

        clock.innerHTML = now.toLocaleString("en-IN", options);

    }

}

setInterval(updateClock,1000);

updateClock();


/*==============================
PRESSURE CHART
==============================*/

const pressureCanvas=document.getElementById("pressureChart");

if(pressureCanvas){

const pressureChart=new Chart(pressureCanvas,{

type:"line",

data:{

labels:chartLabels,


datasets:[{

label:"Pressure",

data:pressureData,

borderColor:"#005bbb",

backgroundColor:"rgba(0,91,187,0.15)",

fill:true,

tension:.4,

borderWidth:3

}]

},

options:{

responsive:true,

plugins:{

legend:{

display:false

}

},

scales:{

y:{

beginAtZero:false

}

}

}

});

}


/*==============================
TEMPERATURE CHART
==============================*/

const tempCanvas=document.getElementById("temperatureChart");

if(tempCanvas){

new Chart(tempCanvas,{

type:"line",

data:{

labels:chartLabels,

datasets:[{

label:"Temperature",

data:temperatureData,

borderColor:"#ff5722",

backgroundColor:"rgba(255,87,34,.15)",

fill:true,

tension:.4,

borderWidth:3

}]

},

options:{

responsive:true,

plugins:{

legend:{

display:false

}

}

}

});

}
/*==============================
ENERGY CONSUMPTION CHART
==============================*/

const energyCanvas = document.getElementById("energyChart");

if (energyCanvas) {

    new Chart(energyCanvas, {

        type: "bar",

        data: {

            labels:chartLabels,

            datasets: [{

                label: "Energy (kWh)",

                data:energyData,

                backgroundColor: [

                    "#005bbb",

                    "#00b894",

                    "#ff9800",

                    "#e53935",

                    "#673ab7"

                ],

                borderRadius: 8

            }]

        },

        options: {

            responsive: true,

            plugins: {

                legend: {

                    display: false

                }

            }

        }

    });

}

/*==============================
AI STATUS PIE CHART
==============================*/

const statusCanvas = document.getElementById("statusChart");

if (statusCanvas) {

    new Chart(statusCanvas, {

        type: "doughnut",

        data: {

            labels: [

                "Normal",

                "Fault"

            ],

            datasets: [{

                data: [normalCount,faultCount],

                backgroundColor: [

                    "#00c853",

                    "#e53935"

                ],

                borderWidth: 0

            }]

        },

        options: {

            responsive: true,

            cutout: "70%",

            plugins: {

                legend: {

                    position: "bottom"

                }

            }

        }

    });

}

/*==============================
ANIMATE SENSOR VALUES
==============================*/

document.querySelectorAll(".sensor-card h1").forEach(function(card){

    card.style.transition="0.4s";

});

/*==============================
CARD HOVER EFFECT
==============================*/

document.querySelectorAll(".sensor-card").forEach(function(card){

    card.addEventListener("mouseenter",function(){

        this.style.transform="translateY(-8px) scale(1.02)";

    });

    card.addEventListener("mouseleave",function(){

        this.style.transform="translateY(0px) scale(1)";

    });

});

/*==============================
AUTO REFRESH CLOCK
==============================*/

setInterval(function(){

    updateClock();

},1000);

console.log("OilSense AI Dashboard Loaded Successfully");

// =========================================
// HEALTH ANIMATION
// =========================================

const healthCircle=document.querySelector(".health-circle");

if(healthCircle){

healthCircle.animate(

[

{transform:"scale(.9)"},

{transform:"scale(1.05)"},

{transform:"scale(1)"}

],

{

duration:1800,

iterations:Infinity

}

);

}
// =========================================
// CARD HOVER EFFECT
// =========================================

document.querySelectorAll(

".overview-card,.sensor-card,.analytics-card,.system-card"

).forEach(card=>{

card.addEventListener("mouseenter",()=>{

card.style.transform="translateY(-8px)";

});

card.addEventListener("mouseleave",()=>{

card.style.transform="translateY(0px)";

});

});
// =========================================
// ALERT SOUND
// =========================================

const alertBox=document.querySelector(".critical");

if(alertBox){

let audio=new Audio("/static/audio/alert.mp3");

audio.volume=.35;

audio.play();

}
window.onload=function(){

document.getElementById("loader").style.display="none";

}
