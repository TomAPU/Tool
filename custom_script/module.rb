#
# Copyright (c) 2006-2019 TomAPU - tomapufckgml@gmail.com
# Browser Exploitation Framework (BeEF) - http://beefproject.com
# See the file 'doc/COPYING' for copying permission
#
class Custom_script < BeEF::Core::Command
  
 # set and return all options for this module
  def self.options
    return [{
      'name' => 'code', 
      'description' => 'Execute custom script ', 
      'type' => 'textarea',
      'ui_label' => 'code',
      'value' => 'alert(1145141919810);',
      'width' => '400px' 
      }]
  end

  def post_execute 
    content = {}
    content['script result'] = @datastore['result']
    save content
  end
  
end
