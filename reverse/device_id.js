function x() {
	var B = {};
	try {
		B.screen_resolution = g.screen.width + ',' + g.screen.height;
		B.available_screen_resolution = g.screen.availWidth + ',' + g.screen.availHeight;
		B.system_version = "unknown";
		B.brand_model = "unknown";
		B.timezone = '';
		B.web_timezone = v;
		B.timezoneOffset = new n().getTimezoneOffset();
		B.user_agent = g.navigator.userAgent;
		B.list_plugin = w().join(',');
		B.platform = g.navigator.platform;
		B.webgl_vendor = "unknown";
		B.webgl_renderer = "unknown";
		var C = JSON.stringify(B);
		return g.btoa(C);
	} catch (E) {
		var D = E.toString();
		return g.btoa(l(D));
	}
}