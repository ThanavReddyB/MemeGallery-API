from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def serve_frontend():
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>memegallery</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap">
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#0a0a0a;--card:#141414;--elevated:#1a1a1a;
  --fg:#e8e6e3;--muted:#6b6b6b;--accent:#c8ff00;
  --border:#222;--danger:#ff4444;--r:12px;
}
body{background:var(--bg);color:var(--fg);font-family:'Inter',sans-serif;min-height:100vh;overflow:hidden}
::selection{background:var(--accent);color:var(--bg)}
::-webkit-scrollbar{height:4px;width:4px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:var(--muted);border-radius:3px}

nav{position:fixed;top:0;left:0;right:0;z-index:100;padding:16px 32px;display:flex;justify-content:space-between;align-items:center;backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);background:rgba(10,10,10,.7);border-bottom:1px solid var(--border)}
.logo{font-family:'Space Grotesk',sans-serif;font-size:1.3rem;font-weight:700;letter-spacing:-.5px}
.logo b{color:var(--accent)}
.nav-right{display:flex;gap:10px;align-items:center}
.nav-email{font-size:.78rem;color:var(--muted);margin-right:6px}

.btn{font-family:'Space Grotesk',sans-serif;font-size:.82rem;font-weight:500;padding:8px 20px;border:1px solid var(--border);border-radius:99px;background:transparent;color:var(--fg);cursor:pointer;transition:all .25s ease}
.btn:hover{background:var(--fg);color:var(--bg);border-color:var(--fg)}
.btn-go{background:var(--accent);color:var(--bg);border-color:var(--accent)}
.btn-go:hover{background:#d4ff33;border-color:#d4ff33}
.btn-x{border-color:var(--danger);color:var(--danger)}
.btn-x:hover{background:var(--danger);color:var(--bg)}
.btn-s{padding:5px 14px;font-size:.73rem}

/* AUTH */
#auth{display:none;min-height:100vh;align-items:center;justify-content:center;padding:40px 20px}
.box{width:100%;max-width:380px}
.box h1{font-family:'Space Grotesk',sans-serif;font-size:2.4rem;font-weight:300;letter-spacing:-1px;margin-bottom:6px}
.box p{color:var(--muted);font-size:.88rem;margin-bottom:32px}
.fg{margin-bottom:16px}
.fg label{display:block;font-size:.72rem;font-family:'Space Grotesk',sans-serif;font-weight:500;text-transform:uppercase;letter-spacing:1.5px;color:var(--muted);margin-bottom:6px}
.fg input{width:100%;padding:12px 14px;background:var(--card);border:1px solid var(--border);border-radius:var(--r);color:var(--fg);font-family:'Inter',sans-serif;font-size:.92rem;outline:none;transition:border .25s}
.fg input:focus{border-color:var(--accent)}
.fg input::placeholder{color:var(--muted)}
.box .btn{width:100%;padding:13px;font-size:.92rem;margin-top:10px}
.sw{text-align:center;margin-top:20px;font-size:.83rem;color:var(--muted)}
.sw a{color:var(--accent);cursor:pointer;text-decoration:none}
.sw a:hover{text-decoration:underline}
.err{color:var(--danger);font-size:.78rem;margin-top:6px;min-height:18px}

/* FEED - horizontal scroll */
#feed{display:none;height:100vh;padding-top:60px}

.scroll-wrap{
  display:flex;
  height:100%;
  overflow-x:auto;
  overflow-y:hidden;
  scroll-snap-type:x mandatory;
  scroll-behavior:smooth;
  -webkit-overflow-scrolling:touch;
}

.slide{
  flex:0 0 100vw;
  scroll-snap-align:center;
  display:flex;
  align-items:center;
  justify-content:center;
  padding:20px;
  height:100%;
}

.slide-inner{
  display:flex;
  gap:40px;
  align-items:center;
  max-width:1100px;
  width:100%;
  height:calc(100vh - 120px);
}

.slide-media{
  flex:1;
  height:100%;
  border-radius:var(--r);
  overflow:hidden;
  background:var(--card);
  cursor:pointer;
  position:relative;
}

.slide-media img,.slide-media video{
  width:100%;
  height:100%;
  object-fit:contain;
  background:var(--bg);
  transition:transform .4s ease;
}

.slide-media:hover img,.slide-media:hover video{
  transform:scale(1.02);
}

.slide-info{
  flex:0 0 280px;
  display:flex;
  flex-direction:column;
  justify-content:center;
  gap:16px;
}

.slide-caption{
  font-size:1.1rem;
  line-height:1.6;
  font-weight:400;
}

.slide-author{
  font-size:.78rem;
  color:var(--muted);
  font-family:'Space Grotesk',sans-serif;
  letter-spacing:.5px;
}

.slide-date{
  font-size:.72rem;
  color:var(--muted);
}

.slide-you{
  display:inline-block;
  font-size:.62rem;
  padding:2px 7px;
  background:var(--accent);
  color:var(--bg);
  border-radius:99px;
  font-family:'Space Grotesk',sans-serif;
  font-weight:600;
  letter-spacing:.5px;
  text-transform:uppercase;
  margin-left:6px;
}

.slide-actions{
  display:flex;
  gap:8px;
  margin-top:8px;
}

/* counter at bottom */
.slide-counter{
  position:fixed;
  bottom:20px;
  left:50%;
  transform:translateX(-50%);
  font-family:'Space Grotesk',sans-serif;
  font-size:.75rem;
  color:var(--muted);
  letter-spacing:2px;
  z-index:50;
}

/* scroll hint arrows */
.scroll-hint{
  position:fixed;
  top:50%;
  transform:translateY(-50%);
  z-index:50;
  background:rgba(20,20,20,.6);
  backdrop-filter:blur(8px);
  border:1px solid var(--border);
  color:var(--fg);
  width:44px;
  height:44px;
  border-radius:50%;
  display:flex;
  align-items:center;
  justify-content:center;
  cursor:pointer;
  font-size:1.2rem;
  transition:all .25s;
}
.scroll-hint:hover{background:var(--fg);color:var(--bg);border-color:var(--fg)}
.scroll-hint.left{left:16px}
.scroll-hint.right{right:16px}

.empty{display:flex;align-items:center;justify-content:center;height:100%;width:100vw;flex-direction:column}
.empty h2{font-family:'Space Grotesk',sans-serif;font-size:1.8rem;font-weight:300;margin-bottom:8px}
.empty p{color:var(--muted);font-size:.88rem}

/* LIGHTBOX */
.lightbox{
  display:none;
  position:fixed;
  inset:0;
  z-index:300;
  background:rgba(0,0,0,.95);
  align-items:center;
  justify-content:center;
  cursor:zoom-out;
}
.lightbox.on{display:flex}
.lightbox img,.lightbox video{
  max-width:95vw;
  max-height:95vh;
  object-fit:contain;
  border-radius:8px;
}

/* modals */
.ov{display:none;position:fixed;inset:0;background:rgba(0,0,0,.8);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);z-index:200;align-items:center;justify-content:center;padding:20px}
.ov.on{display:flex}
.md{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:32px;width:100%;max-width:460px}
.md h2{font-family:'Space Grotesk',sans-serif;font-size:1.6rem;font-weight:300;margin-bottom:20px}
.md .btn{width:100%;margin-top:6px}
.md-x{float:right;background:none;border:none;color:var(--muted);font-size:1.4rem;cursor:pointer;line-height:1}
.md-x:hover{color:var(--fg)}

.drop{border:2px dashed var(--border);border-radius:var(--r);padding:36px;text-align:center;cursor:pointer;transition:all .25s;margin-bottom:16px}
.drop:hover,.drop.over{border-color:var(--accent);background:rgba(200,255,0,.03)}
.drop .ic{font-size:1.8rem;margin-bottom:8px;opacity:.5}
.drop .tx{font-size:.82rem;color:var(--muted)}
.drop .tx b{color:var(--accent)}
.fn{font-size:.78rem;color:var(--accent);margin-top:6px}

.cov{display:none;position:fixed;inset:0;background:rgba(0,0,0,.8);backdrop-filter:blur(10px);z-index:250;align-items:center;justify-content:center;padding:20px}
.cov.on{display:flex}
.cbox{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:28px;max-width:360px;width:100%;text-align:center}
.cbox h3{font-family:'Space Grotesk',sans-serif;font-size:1.2rem;font-weight:400;margin-bottom:6px}
.cbox p{color:var(--muted);font-size:.82rem;margin-bottom:20px}
.cbox .acts{display:flex;gap:10px}
.cbox .acts .btn{flex:1}

.spin{display:inline-block;width:16px;height:16px;border:2px solid var(--border);border-top-color:var(--accent);border-radius:50%;animation:sp .7s linear infinite;vertical-align:middle;margin-right:6px}
@keyframes sp{to{transform:rotate(360deg)}}

.toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%) translateY(80px);background:var(--elevated);border:1px solid var(--border);color:var(--fg);padding:12px 24px;border-radius:99px;font-size:.82rem;font-family:'Space Grotesk',sans-serif;z-index:400;transition:transform .35s ease;pointer-events:none}
.toast.on{transform:translateX(-50%) translateY(0)}

@media(max-width:768px){
  nav{padding:14px 16px}
  .slide{padding:10px}
  .slide-inner{flex-direction:column;gap:16px;height:auto;padding-top:10px}
  .slide-media{flex:none;width:100%;height:50vh}
  .slide-info{flex:none;width:100%;padding:0 10px 20px}
  .scroll-hint{display:none}
  .box h1{font-size:1.8rem}
  .md{padding:20px}
}
</style>
</head>
<body>
<div class="toast" id="toast"></div>

<nav>
  <div class="logo">meme<b>gallery</b></div>
  <div class="nav-right">
    <span class="nav-email" id="nav-email"></span>
    <button class="btn btn-s" id="btn-up" style="display:none">Upload</button>
    <button class="btn btn-s" id="btn-out" style="display:none">Logout</button>
  </div>
</nav>

<div id="auth">
  <div class="box" id="login-box">
    <h1>Welcome back</h1>
    <p>Sign in to continue</p>
    <div class="fg"><label for="le">Email</label><input type="email" id="le" placeholder="your@email.com"></div>
    <div class="fg"><label for="lp">Password</label><input type="password" id="lp" placeholder="Enter password"></div>
    <div class="err" id="lerr"></div>
    <button class="btn btn-go" id="lbtn">Sign In</button>
    <div class="sw">No account? <a id="go-reg">Create one</a></div>
  </div>
  <div class="box" id="reg-box" style="display:none">
    <h1>Create account</h1>
    <p>Join and start posting</p>
    <div class="fg"><label for="re">Email</label><input type="email" id="re" placeholder="your@email.com"></div>
    <div class="fg"><label for="rp">Password</label><input type="password" id="rp" placeholder="Min 8 characters"></div>
    <div class="err" id="rerr"></div>
    <button class="btn btn-go" id="rbtn">Create Account</button>
    <div class="sw">Have an account? <a id="go-login">Sign in</a></div>
  </div>
</div>

<div id="feed">
  <div class="scroll-wrap" id="scroll-wrap"></div>
  <button class="scroll-hint left" id="arr-l">&#8592;</button>
  <button class="scroll-hint right" id="arr-r">&#8594;</button>
  <div class="slide-counter" id="counter"></div>
</div>

<div class="lightbox" id="lightbox"></div>

<div class="ov" id="umod">
  <div class="md">
    <button class="md-x" id="umod-x">&times;</button>
    <h2>New post</h2>
    <div class="drop" id="drop">
      <div class="ic">+</div>
      <div class="tx">Drop a file or <b>browse</b></div>
      <div class="fn" id="fname"></div>
    </div>
    <input type="file" id="finput" accept="image/*,video/*" style="display:none">
    <div class="fg"><label for="ucap">Caption</label><input type="text" id="ucap" placeholder="Write a caption..."></div>
    <div class="err" id="uerr"></div>
    <button class="btn btn-go" id="ubtn">Publish</button>
  </div>
</div>

<div class="cov" id="cdel">
  <div class="cbox">
    <h3>Delete post?</h3>
    <p>This action cannot be undone.</p>
    <div class="acts">
      <button class="btn btn-s" id="cdel-no">Cancel</button>
      <button class="btn btn-s btn-x" id="cdel-yes">Delete</button>
    </div>
  </div>
</div>

<script>
(function(){
  var token = null, delId = null, file = null, currentSlide = 0, totalSlides = 0;
  try { token = localStorage.getItem('token'); } catch(e) {}
  var $ = function(id){ return document.getElementById(id); };

  function toast(m){
    var t=$('toast');t.textContent=m;t.classList.add('on');
    setTimeout(function(){t.classList.remove('on');},2500);
  }
  function esc(s){var d=document.createElement('div');d.textContent=s;return d.innerHTML;}

  // AUTH
  function showAuth(){
    $('auth').style.display='flex';$('feed').style.display='none';
    $('btn-up').style.display='none';$('btn-out').style.display='none';
    $('nav-email').textContent='';document.body.style.overflow='hidden';
  }
  function showLogin(){$('login-box').style.display='block';$('reg-box').style.display='none';}
  function showReg(){$('login-box').style.display='none';$('reg-box').style.display='block';}

  $('go-reg').onclick=showReg;
  $('go-login').onclick=showLogin;

  $('lbtn').onclick=function(){
    var email=$('le').value,pw=$('lp').value,err=$('lerr'),btn=$('lbtn');
    err.textContent='';
    if(!email||!pw){err.textContent='Fill in all fields';return;}
    btn.innerHTML='<span class="spin"></span>Signing in...';btn.disabled=true;
    var form=new URLSearchParams();form.append('username',email);form.append('password',pw);
    fetch('/auth/jwt/login',{method:'POST',body:form})
      .then(function(r){return r.json().then(function(d){return{ok:r.ok,data:d};});})
      .then(function(r){
        if(!r.ok)throw new Error(r.data.detail||'Invalid credentials');
        token=r.data.access_token;
        try{localStorage.setItem('token',token);}catch(e){}
        toast('Welcome back');showFeed();
      })
      .catch(function(e){err.textContent=e.message;})
      .finally(function(){btn.innerHTML='Sign In';btn.disabled=false;});
  };

  $('rbtn').onclick=function(){
    var email=$('re').value,pw=$('rp').value,err=$('rerr'),btn=$('rbtn');
    err.textContent='';
    if(!email||!pw){err.textContent='Fill in all fields';return;}
    if(pw.length<8){err.textContent='Password must be at least 8 characters';return;}
    btn.innerHTML='<span class="spin"></span>Creating...';btn.disabled=true;
    fetch('/auth/register',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:email,password:pw})})
      .then(function(r){return r.json().then(function(d){return{ok:r.ok,data:d};});})
      .then(function(r){
        if(!r.ok)throw new Error(r.data.detail||'Registration failed');
        toast('Account created — sign in now');showLogin();
      })
      .catch(function(e){err.textContent=e.message;})
      .finally(function(){btn.innerHTML='Create Account';btn.disabled=false;});
  };

  $('btn-out').onclick=function(){
    token=null;try{localStorage.removeItem('token');}catch(e){}
    showAuth();toast('Signed out');
  };

  $('le').onkeydown=$('lp').onkeydown=function(e){if(e.key==='Enter')$('lbtn').click();};
  $('re').onkeydown=$('rp').onkeydown=function(e){if(e.key==='Enter')$('rbtn').click();};
  $('ucap').onkeydown=function(e){if(e.key==='Enter')$('ubtn').click();};

  // FEED
  function showFeed(){
    $('auth').style.display='none';$('feed').style.display='block';
    $('btn-up').style.display='';$('btn-out').style.display='';
    document.body.style.overflow='hidden';
    loadFeed();
  }

  function updateCounter(){
    if(totalSlides>0) $('counter').textContent=(currentSlide+1)+' / '+totalSlides;
    else $('counter').textContent='';
  }

  function scrollToSlide(i){
    if(i<0||i>=totalSlides)return;
    currentSlide=i;
    var wrap=$('scroll-wrap');
    wrap.children[i].scrollIntoView({behavior:'smooth',inline:'center',block:'nearest'});
    updateCounter();
  }

  $('arr-l').onclick=function(){scrollToSlide(currentSlide-1);};
  $('arr-r').onclick=function(){scrollToSlide(currentSlide+1);};

  // track current slide on scroll
  var scrollTimer;
  $('scroll-wrap').addEventListener('scroll',function(){
    clearTimeout(scrollTimer);
    scrollTimer=setTimeout(function(){
      var wrap=$('scroll-wrap');
      var center=wrap.scrollLeft+wrap.clientWidth/2;
      var slides=wrap.children;
      var closest=0,minDist=Infinity;
      for(var i=0;i<slides.length;i++){
        var dist=Math.abs(slides[i].offsetLeft+slides[i].clientWidth/2-center);
        if(dist<minDist){minDist=dist;closest=i;}
      }
      currentSlide=closest;
      updateCounter();
    },100);
  });

  // keyboard nav
  document.addEventListener('keydown',function(e){
    if($('feed').style.display==='none')return;
    if($('umod').classList.contains('on')||$('cdel').classList.contains('on'))return;
    if($('lightbox').classList.contains('on')){
      if(e.key==='Escape')$('lightbox').classList.remove('on');
      return;
    }
    if(e.key==='ArrowRight')scrollToSlide(currentSlide+1);
    if(e.key==='ArrowLeft')scrollToSlide(currentSlide-1);
  });

  function loadFeed(){
    var wrap=$('scroll-wrap');
    wrap.innerHTML='<div class="empty"><span class="spin"></span> Loading...</div>';
    $('counter').textContent='';

    fetch('/feed',{headers:{'Authorization':'Bearer '+token}})
      .then(function(r){
        if(r.status===401){token=null;try{localStorage.removeItem('token');}catch(e){}showAuth();throw new Error('__auth__');}
        return r.json();
      })
      .then(function(data){
        var posts=data.posts||[];
        totalSlides=posts.length;
        currentSlide=0;

        var own=posts.filter(function(p){return p.is_owner;});
        if(own.length)$('nav-email').textContent=own[0].email||'';

        if(!posts.length){
          wrap.innerHTML='<div class="empty"><h2>Nothing here yet</h2><p>Upload your first meme</p></div>';
          $('arr-l').style.display='none';$('arr-r').style.display='none';
          return;
        }
        $('arr-l').style.display='';$('arr-r').style.display='';

        wrap.innerHTML=posts.map(function(p){
          var media=p.file_type==='video'
            ?'<video src="'+esc(p.url)+'" muted loop playsinline data-src="'+esc(p.url)+'"></video>'
            :'<img src="'+esc(p.url)+'" alt="'+esc(p.caption||'')+'" loading="lazy" data-src="'+esc(p.url)+'" data-type="image">';
          var dt=p.created_at?new Date(p.created_at).toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'}):'';
          var del=p.is_owner?'<button class="btn btn-s btn-x" data-del="'+p.id+'">Delete</button>':'';

          return '<div class="slide"><div class="slide-inner">'
            +'<div class="slide-media" data-type="'+(p.file_type||'image')+'">'+media+'</div>'
            +'<div class="slide-info">'
            +'<div class="slide-caption">'+esc(p.caption||'')+'</div>'
            +'<div class="slide-author">'+esc(p.email||'Anonymous')
            +(p.is_owner?'<span class="slide-you">You</span>':'')+'</div>'
            +'<div class="slide-date">'+dt+'</div>'
            +(del?'<div class="slide-actions">'+del+'</div>':'')
            +'</div></div></div>';
        }).join('');

        updateCounter();

        // click media to open lightbox
        wrap.querySelectorAll('.slide-media').forEach(function(el){
          el.onclick=function(){
            var lb=$('lightbox');
            var src=el.querySelector('img,video');
            if(el.getAttribute('data-type')==='video'){
              lb.innerHTML='<video src="'+src.getAttribute('data-src')+'" controls autoplay style="max-width:95vw;max-height:95vh;border-radius:8px"></video>';
            } else {
              lb.innerHTML='<img src="'+src.getAttribute('data-src')+'" style="max-width:95vw;max-height:95vh;object-fit:contain;border-radius:8px">';
            }
            lb.classList.add('on');
          };
        });

        // video hover play
        wrap.querySelectorAll('video').forEach(function(v){
          var slide=v.closest('.slide');
          slide.onmouseenter=function(){v.play();};
          slide.onmouseleave=function(){v.pause();};
        });

        // delete buttons
        wrap.querySelectorAll('[data-del]').forEach(function(b){
          b.onclick=function(e){e.stopPropagation();delId=b.getAttribute('data-del');$('cdel').classList.add('on');};
        });
      })
      .catch(function(e){if(e.message!=='__auth__')wrap.innerHTML='<div class="empty"><h2>Error</h2><p>'+esc(e.message)+'</p></div>';});
  }

  // LIGHTBOX close
  $('lightbox').onclick=function(){$('lightbox').classList.remove('on');$('lightbox').innerHTML='';};

  // UPLOAD
  $('btn-up').onclick=function(){
    file=null;$('finput').value='';$('fname').textContent='';
    $('ucap').value='';$('uerr').textContent='';
    $('umod').classList.add('on');
  };
  $('umod-x').onclick=function(){$('umod').classList.remove('on');};
  $('drop').onclick=function(){$('finput').click();};
  $('finput').onchange=function(){if(this.files.length){file=this.files[0];$('fname').textContent=file.name;}};

  var dz=$('drop');
  dz.ondragover=function(e){e.preventDefault();dz.classList.add('over');};
  dz.ondragleave=function(){dz.classList.remove('over');};
  dz.ondrop=function(e){e.preventDefault();dz.classList.remove('over');if(e.dataTransfer.files.length){file=e.dataTransfer.files[0];$('fname').textContent=file.name;}};

  $('ubtn').onclick=function(){
    var err=$('uerr'),btn=$('ubtn');err.textContent='';
    if(!file){err.textContent='Select a file first';return;}
    btn.innerHTML='<span class="spin"></span>Uploading...';btn.disabled=true;
    var fd=new FormData();fd.append('file',file);fd.append('caption',$('ucap').value);
    fetch('/upload',{method:'POST',headers:{'Authorization':'Bearer '+token},body:fd})
      .then(function(r){return r.json().then(function(d){return{ok:r.ok,data:d};});})
      .then(function(r){
        if(!r.ok)throw new Error(r.data.detail||'Upload failed');
        $('umod').classList.remove('on');toast('Post published');loadFeed();
      })
      .catch(function(e){err.textContent=e.message;})
      .finally(function(){btn.innerHTML='Publish';btn.disabled=false;});
  };

  // DELETE
  $('cdel-no').onclick=function(){delId=null;$('cdel').classList.remove('on');};
  $('cdel-yes').onclick=function(){
    if(!delId)return;var btn=$('cdel-yes');
    btn.innerHTML='<span class="spin"></span>';btn.disabled=true;
    fetch('/posts/'+delId,{method:'DELETE',headers:{'Authorization':'Bearer '+token}})
      .then(function(r){return r.json().then(function(d){return{ok:r.ok,data:d};});})
      .then(function(r){
        if(!r.ok)throw new Error(r.data.detail||'Delete failed');
        delId=null;$('cdel').classList.remove('on');toast('Post deleted');loadFeed();
      })
      .catch(function(e){toast('Error: '+e.message);})
      .finally(function(){btn.innerHTML='Delete';btn.disabled=false;});
  };

  // START
  if(token){showFeed();}else{showAuth();}
})();
</script>
</body>
</html>"""
