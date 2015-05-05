function quati_Manager(){
  var $intern_0 = '', $intern_27 = '" for "gwt:onLoadErrorFn"', $intern_25 = '" for "gwt:onPropertyErrorFn"', $intern_10 = '"><\/script>', $intern_12 = '#', $intern_14 = '/', $intern_45 = '5C40B03E56A2C3BCAAA5B022826446B2.cache.html', $intern_63 = '<script defer="defer">quati_Manager.onInjectionDone(\'quati.Manager\')<\/script>', $intern_9 = '<script id="', $intern_59 = '<script language="javascript" src="', $intern_22 = '=', $intern_13 = '?', $intern_24 = 'Bad handler "', $intern_46 = 'DF9507A4BA902D419DC86EB5DDD6E7B3.cache.html', $intern_57 = 'DOMContentLoaded', $intern_44 = 'FCCE2B88667168E88A66DB621FF61892.cache.html', $intern_47 = 'GwtExt.css', $intern_56 = 'Quati.css', $intern_11 = 'SCRIPT', $intern_8 = '__gwt_marker_quati.Manager', $intern_15 = 'base', $intern_4 = 'begin', $intern_3 = 'bootstrap', $intern_17 = 'clear.cache.gif', $intern_21 = 'content', $intern_7 = 'end', $intern_38 = 'gecko', $intern_39 = 'gecko1_8', $intern_5 = 'gwt.hybrid', $intern_53 = 'gwt/standard/standard.css', $intern_26 = 'gwt:onLoadErrorFn', $intern_23 = 'gwt:onPropertyErrorFn', $intern_20 = 'gwt:property', $intern_52 = 'head', $intern_43 = 'hosted.html?quati_Manager', $intern_51 = 'href', $intern_37 = 'ie6', $intern_28 = 'iframe', $intern_16 = 'img', $intern_29 = "javascript:''", $intern_58 = 'js/ext/adapter/ext/ext-base.js', $intern_60 = 'js/ext/adapter/ext/ext-base.js"><\/script>', $intern_61 = 'js/ext/ext-all.js', $intern_62 = 'js/ext/ext-all.js"><\/script>', $intern_54 = 'js/ext/resources/css/ext-all.css', $intern_55 = 'js/ext/resources/css/xtheme-gray.css', $intern_48 = 'link', $intern_41 = 'loadExternalRefs', $intern_18 = 'meta', $intern_31 = 'moduleRequested', $intern_6 = 'moduleStartup', $intern_36 = 'msie', $intern_19 = 'name', $intern_33 = 'opera', $intern_30 = 'position:absolute;width:0;height:0;border:none', $intern_1 = 'quati.Manager', $intern_49 = 'rel', $intern_35 = 'safari', $intern_42 = 'selectingPermutation', $intern_2 = 'startup', $intern_50 = 'stylesheet', $intern_40 = 'unknown', $intern_32 = 'user.agent', $intern_34 = 'webkit';
  var $wnd = window, $doc = document, $stats = $wnd.__gwtStatsEvent?function(a){
    return $wnd.__gwtStatsEvent(a);
  }
  :null, scriptsDone, loadDone, bodyDone, base = $intern_0, metaProps = {}, values = [], providers = [], answers = [], onLoadErrorFunc, propertyErrorFunc;
  $stats && $stats({moduleName:$intern_1, subSystem:$intern_2, evtGroup:$intern_3, millis:(new Date()).getTime(), type:$intern_4});
  if (!$wnd.__gwt_stylesLoaded) {
    $wnd.__gwt_stylesLoaded = {};
  }
  if (!$wnd.__gwt_scriptsLoaded) {
    $wnd.__gwt_scriptsLoaded = {};
  }
  function isHostedMode(){
    try {
      return $wnd.external && ($wnd.external.gwtOnLoad && $wnd.location.search.indexOf($intern_5) == -1);
    }
     catch (e) {
      return false;
    }
  }

  function maybeStartModule(){
    if (scriptsDone && loadDone) {
      var iframe = $doc.getElementById($intern_1);
      var frameWnd = iframe.contentWindow;
      frameWnd.__gwt_initHandlers = quati_Manager.__gwt_initHandlers;
      if (isHostedMode()) {
        frameWnd.__gwt_getProperty = function(name){
          return computePropValue(name);
        }
        ;
      }
      quati_Manager = null;
      frameWnd.gwtOnLoad(onLoadErrorFunc, $intern_1, base);
      $stats && $stats({moduleName:$intern_1, subSystem:$intern_2, evtGroup:$intern_6, millis:(new Date()).getTime(), type:$intern_7});
    }
  }

  function computeScriptBase(){
    var thisScript, markerId = $intern_8, markerScript;
    $doc.write($intern_9 + markerId + $intern_10);
    markerScript = $doc.getElementById(markerId);
    thisScript = markerScript && markerScript.previousSibling;
    while (thisScript && thisScript.tagName != $intern_11) {
      thisScript = thisScript.previousSibling;
    }
    function getDirectoryOfFile(path){
      var hashIndex = path.lastIndexOf($intern_12);
      if (hashIndex == -1) {
        hashIndex = path.length;
      }
      var queryIndex = path.indexOf($intern_13);
      if (queryIndex == -1) {
        queryIndex = path.length;
      }
      var slashIndex = path.lastIndexOf($intern_14, Math.min(queryIndex, hashIndex));
      return slashIndex >= 0?path.substring(0, slashIndex + 1):$intern_0;
    }

    ;
    if (thisScript && thisScript.src) {
      base = getDirectoryOfFile(thisScript.src);
    }
    if (base == $intern_0) {
      var baseElements = $doc.getElementsByTagName($intern_15);
      if (baseElements.length > 0) {
        base = baseElements[baseElements.length - 1].href;
      }
       else {
        base = getDirectoryOfFile($doc.location.href);
      }
    }
     else if (base.match(/^\w+:\/\//)) {
    }
     else {
      var img = $doc.createElement($intern_16);
      img.src = base + $intern_17;
      base = getDirectoryOfFile(img.src);
    }
    if (markerScript) {
      markerScript.parentNode.removeChild(markerScript);
    }
  }

  function processMetas(){
    var metas = document.getElementsByTagName($intern_18);
    for (var i = 0, n = metas.length; i < n; ++i) {
      var meta = metas[i], name = meta.getAttribute($intern_19), content;
      if (name) {
        if (name == $intern_20) {
          content = meta.getAttribute($intern_21);
          if (content) {
            var value, eq = content.indexOf($intern_22);
            if (eq >= 0) {
              name = content.substring(0, eq);
              value = content.substring(eq + 1);
            }
             else {
              name = content;
              value = $intern_0;
            }
            metaProps[name] = value;
          }
        }
         else if (name == $intern_23) {
          content = meta.getAttribute($intern_21);
          if (content) {
            try {
              propertyErrorFunc = eval(content);
            }
             catch (e) {
              alert($intern_24 + content + $intern_25);
            }
          }
        }
         else if (name == $intern_26) {
          content = meta.getAttribute($intern_21);
          if (content) {
            try {
              onLoadErrorFunc = eval(content);
            }
             catch (e) {
              alert($intern_24 + content + $intern_27);
            }
          }
        }
      }
    }
  }

  function unflattenKeylistIntoAnswers(propValArray, value){
    var answer = answers;
    for (var i = 0, n = propValArray.length - 1; i < n; ++i) {
      answer = answer[propValArray[i]] || (answer[propValArray[i]] = []);
    }
    answer[propValArray[n]] = value;
  }

  function computePropValue(propName){
    var value = providers[propName](), allowedValuesMap = values[propName];
    if (value in allowedValuesMap) {
      return value;
    }
    var allowedValuesList = [];
    for (var k in allowedValuesMap) {
      allowedValuesList[allowedValuesMap[k]] = k;
    }
    if (propertyErrorFunc) {
      propertyErrorFunc(propName, allowedValuesList, value);
    }
    throw null;
  }

  var frameInjected;
  function maybeInjectFrame(){
    if (!frameInjected) {
      frameInjected = true;
      var iframe = $doc.createElement($intern_28);
      iframe.src = $intern_29;
      iframe.id = $intern_1;
      iframe.style.cssText = $intern_30;
      iframe.tabIndex = -1;
      $doc.body.appendChild(iframe);
      $stats && $stats({moduleName:$intern_1, subSystem:$intern_2, evtGroup:$intern_6, millis:(new Date()).getTime(), type:$intern_31});
      iframe.contentWindow.location.replace(base + strongName);
    }
  }

  providers[$intern_32] = function(){
    var ua = navigator.userAgent.toLowerCase();
    var makeVersion = function(result){
      return parseInt(result[1]) * 1000 + parseInt(result[2]);
    }
    ;
    if (ua.indexOf($intern_33) != -1) {
      return $intern_33;
    }
     else if (ua.indexOf($intern_34) != -1) {
      return $intern_35;
    }
     else if (ua.indexOf($intern_36) != -1) {
      var result = /msie ([0-9]+)\.([0-9]+)/.exec(ua);
      if (result && result.length == 3) {
        if (makeVersion(result) >= 6000) {
          return $intern_37;
        }
      }
    }
     else if (ua.indexOf($intern_38) != -1) {
      var result = /rv:([0-9]+)\.([0-9]+)/.exec(ua);
      if (result && result.length == 3) {
        if (makeVersion(result) >= 1008)
          return $intern_39;
      }
      return $intern_38;
    }
    return $intern_40;
  }
  ;
  values[$intern_32] = {gecko:0, gecko1_8:1, ie6:2, opera:3, safari:4};
  quati_Manager.onScriptLoad = function(){
    if (frameInjected) {
      loadDone = true;
      maybeStartModule();
    }
  }
  ;
  quati_Manager.onInjectionDone = function(){
    scriptsDone = true;
    $stats && $stats({moduleName:$intern_1, subSystem:$intern_2, evtGroup:$intern_41, millis:(new Date()).getTime(), type:$intern_7});
    maybeStartModule();
  }
  ;
  computeScriptBase();
  processMetas();
  $stats && $stats({moduleName:$intern_1, subSystem:$intern_2, evtGroup:$intern_3, millis:(new Date()).getTime(), type:$intern_42});
  var strongName;
  if (isHostedMode()) {
    strongName = $intern_43;
  }
   else {
    try {
      unflattenKeylistIntoAnswers([$intern_33], $intern_44);
      unflattenKeylistIntoAnswers([$intern_35], $intern_44);
      unflattenKeylistIntoAnswers([$intern_37], $intern_45);
      unflattenKeylistIntoAnswers([$intern_38], $intern_46);
      unflattenKeylistIntoAnswers([$intern_39], $intern_46);
      strongName = answers[computePropValue($intern_32)];
    }
     catch (e) {
      return;
    }
  }
  var onBodyDoneTimerId;
  function onBodyDone(){
    if (!bodyDone) {
      bodyDone = true;
      if (!__gwt_stylesLoaded[$intern_47]) {
        var l = $doc.createElement($intern_48);
        __gwt_stylesLoaded[$intern_47] = l;
        l.setAttribute($intern_49, $intern_50);
        l.setAttribute($intern_51, base + $intern_47);
        $doc.getElementsByTagName($intern_52)[0].appendChild(l);
      }
      if (!__gwt_stylesLoaded[$intern_53]) {
        var l = $doc.createElement($intern_48);
        __gwt_stylesLoaded[$intern_53] = l;
        l.setAttribute($intern_49, $intern_50);
        l.setAttribute($intern_51, base + $intern_53);
        $doc.getElementsByTagName($intern_52)[0].appendChild(l);
      }
      if (!__gwt_stylesLoaded[$intern_54]) {
        var l = $doc.createElement($intern_48);
        __gwt_stylesLoaded[$intern_54] = l;
        l.setAttribute($intern_49, $intern_50);
        l.setAttribute($intern_51, base + $intern_54);
        $doc.getElementsByTagName($intern_52)[0].appendChild(l);
      }
      if (!__gwt_stylesLoaded[$intern_55]) {
        var l = $doc.createElement($intern_48);
        __gwt_stylesLoaded[$intern_55] = l;
        l.setAttribute($intern_49, $intern_50);
        l.setAttribute($intern_51, base + $intern_55);
        $doc.getElementsByTagName($intern_52)[0].appendChild(l);
      }
      if (!__gwt_stylesLoaded[$intern_56]) {
        var l = $doc.createElement($intern_48);
        __gwt_stylesLoaded[$intern_56] = l;
        l.setAttribute($intern_49, $intern_50);
        l.setAttribute($intern_51, base + $intern_56);
        $doc.getElementsByTagName($intern_52)[0].appendChild(l);
      }
      maybeStartModule();
      if ($doc.removeEventListener) {
        $doc.removeEventListener($intern_57, onBodyDone, false);
      }
      if (onBodyDoneTimerId) {
        clearInterval(onBodyDoneTimerId);
      }
    }
  }

  if ($doc.addEventListener) {
    $doc.addEventListener($intern_57, function(){
      maybeInjectFrame();
      onBodyDone();
    }
    , false);
  }
  var onBodyDoneTimerId = setInterval(function(){
    if (/loaded|complete/.test($doc.readyState)) {
      maybeInjectFrame();
      onBodyDone();
    }
  }
  , 50);
  $stats && $stats({moduleName:$intern_1, subSystem:$intern_2, evtGroup:$intern_3, millis:(new Date()).getTime(), type:$intern_7});
  $stats && $stats({moduleName:$intern_1, subSystem:$intern_2, evtGroup:$intern_41, millis:(new Date()).getTime(), type:$intern_4});
  if (!__gwt_scriptsLoaded[$intern_58]) {
    __gwt_scriptsLoaded[$intern_58] = true;
    document.write($intern_59 + base + $intern_60);
  }
  if (!__gwt_scriptsLoaded[$intern_61]) {
    __gwt_scriptsLoaded[$intern_61] = true;
    document.write($intern_59 + base + $intern_62);
  }
  $doc.write($intern_63);
}

quati_Manager.__gwt_initHandlers = function(resize, beforeunload, unload){
  var $wnd = window, oldOnResize = $wnd.onresize, oldOnBeforeUnload = $wnd.onbeforeunload, oldOnUnload = $wnd.onunload;
  $wnd.onresize = function(evt){
    try {
      resize();
    }
     finally {
      oldOnResize && oldOnResize(evt);
    }
  }
  ;
  $wnd.onbeforeunload = function(evt){
    var ret, oldRet;
    try {
      ret = beforeunload();
    }
     finally {
      oldRet = oldOnBeforeUnload && oldOnBeforeUnload(evt);
    }
    if (ret != null) {
      return ret;
    }
    if (oldRet != null) {
      return oldRet;
    }
  }
  ;
  $wnd.onunload = function(evt){
    try {
      unload();
    }
     finally {
      oldOnUnload && oldOnUnload(evt);
      $wnd.onresize = null;
      $wnd.onbeforeunload = null;
      $wnd.onunload = null;
    }
  }
  ;
}
;
quati_Manager();
