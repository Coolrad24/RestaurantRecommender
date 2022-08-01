const name=document.getElementById('nm');
const address=document.getElementById('ad');
const button=document.getElementById('go');
/*
function getInput(){
    const name=document.getElementById('nm');
    const address=document.getElementById('ad');
    var Name=name.value;
    var Address=address.value
    var data=Name+"  "+Address;
    fetch('http://127.0.0.1:5000/restaurant',{
        method:'POST',
        headers: {
            'Content-type': 'application/json',
            'Accept': 'application/json'
        },
        body:JSON.stringify(data)}).then(res=>{
            if(res.ok){
                return res.json()
            }else{
                alert('wrong')
            }
        }).then(jsonResponse=>{
            console.log(jsonResponse)
        }
        ).catch((err)=>console.log(error));
    
    

}

*/