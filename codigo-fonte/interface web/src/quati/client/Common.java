package quati.client;

import com.gwtext.client.data.Store;

public class Common {

	public static native String convertTime(String unixtime) /*-{
		date = new Date();
		var mEpoch = parseInt(unixtime);
		if(mEpoch<10000000000) mEpoch *= 1000; 
		// convert to milliseconds (Epoch is usually expressed in seconds, but Javascript uses Milliseconds)
		date.setTime(mEpoch);
		var month = date.getMonth()+1;
		
		return $wnd.sprintf("%d/%02d/%02d %02d:%02d:%02d",date.getFullYear(),month,date.getDate(),date.getHours(),date.getMinutes(),date.getSeconds());
		
	}-*/;
	
	public static native void prepareAndLoadStore(Store store) /*-{
		var store = store.@com.gwtext.client.core.JsObject::getJsObj()();
		
		store.on({'loadexception':{
		            fn: function(httpProxy, dataObject, arguments, exception){
		            	alert("error:"+exception+" args:"+arguments);
		            }
		            ,scope:this
		            ,delay:0
		       		}
		});

		store.load();
	
	}-*/;
	
}
