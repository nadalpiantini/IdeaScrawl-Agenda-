// ID: CNT-001-V01
// content.js
const titleEl = document.querySelector('h1');
const chatTitle = titleEl?.innerText||'Sin título';

const observer = new MutationObserver(ms=>{
  ms.forEach(m=>{
    m.addedNodes.forEach(n=>{
      if(n.nodeType===1 && n.matches('.group > div')){
        const text=n.innerText.trim();
        chrome.runtime.sendMessage({type:'newMessage',chatTitle,text});
      }
    });
  });
});
observer.observe(document.body,{childList:true,subtree:true});
