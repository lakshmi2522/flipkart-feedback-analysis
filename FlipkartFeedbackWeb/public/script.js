const form=document.getElementById("form"), feedback=document.getElementById("feedback");
const counter=document.getElementById("counter"), message=document.getElementById("message");
feedback.addEventListener("input",()=>{counter.textContent=`${feedback.value.length} / 500`;counter.style.color=feedback.value.length>500?"#bd342b":""});
form.addEventListener("submit",async e=>{
 e.preventDefault();message.textContent="";message.style.color="#bd342b";
 const data=new URLSearchParams(new FormData(form));
 if(!document.getElementById("name").value.trim()){message.textContent="Please enter the customer name.";return}
 if(!feedback.value.trim()){message.textContent="Feedback cannot be empty.";return}
 if(feedback.value.trim().length>500){message.textContent="Feedback cannot exceed 500 characters.";return}
 const button=document.getElementById("submit");button.disabled=true;button.textContent="Analyzing...";
 try{
  const res=await fetch("/api/analyze",{method:"POST",headers:{"Content-Type":"application/x-www-form-urlencoded;charset=UTF-8"},body:data.toString()});
  const result=await res.json();if(!res.ok){message.textContent=result.error||"Unable to analyze.";return}
  document.getElementById("chars").textContent=result.characterCount;
  document.getElementById("words").textContent=result.wordCount;
  document.getElementById("matches").textContent=result.occurrences;
  document.getElementById("keylabel").textContent=result.keyword?`Keyword: ${result.keyword}`:"Keyword: not entered";
  document.getElementById("customer").textContent=`Customer: ${result.customerName}`;
  document.getElementById("messageText").textContent=result.feedback;
  document.getElementById("searchNote").textContent=result.keyword?`Found ${result.occurrences} occurrence(s) of “${result.keyword}” using case-insensitive search.`:"No keyword entered; keyword search was skipped.";
  document.getElementById("empty").classList.add("hidden");document.getElementById("results").classList.remove("hidden");
  message.textContent="Feedback analyzed successfully.";message.style.color="#16875d";
 }catch(err){message.textContent="Cannot connect to Java server. Check that it is running."}
 finally{button.disabled=false;button.innerHTML='Analyze feedback <b>→</b>'}
});