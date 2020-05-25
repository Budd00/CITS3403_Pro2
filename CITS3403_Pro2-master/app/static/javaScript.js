var preset,inputs;
init();
function init(){
    inputs=document.getElementsByClassName("a");
    var bn=document.getElementById("bn");
    var div=document.getElementById("div0");
    for(var i=0;i<inputs.length;i++){
        inputs[i].oninput=inputHandler;//call input handler while input
    }
    
    bn.onclick=clickHandler;
    setInterval(animation,500,div);
}
function inputHandler(){
    this.value=this.value.replace(/\D/g,"");//num only
}
function clickHandler(){//click to get current time and fill time
    preset=new Date();
    preset.setHours(preset.getHours()+Number(inputs[0].value));
    preset.setMinutes(preset.getMinutes()+Number(inputs[1].value));
    preset.setSeconds(preset.getSeconds()+Number(inputs[2].value));
    setDisabled(true);
    
}
function animation(elem){
    if(!preset) return;//if no time
    var date=new Date();
    var time=preset-date;//
    if(time<0){
        preset=null;
        setDisabled(false);
        return;
    }
    time=time/1000;
    var h=time>=3600 ? parseInt(time/3600) : 0;
    var m=time>=60 ? parseInt((time-h*3600)/60) : 0;
    var s=parseInt(time-h*3600-m*60);
    elem.innerHTML=h+"小时"+m+"分"+s+"秒";
}

function setDisabled(bool){
    for(var i=0;i<inputs.length;i++){
        inputs[i].disabled=bool;
    }
}
