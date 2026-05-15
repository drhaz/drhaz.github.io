---
layout: page
title: Contact
description:  Leave a message
comments: false
---

Please leave a message below.<br>
Note: The message will be sent via
a forwarding service (formspree.io), but will be encrypted via gpg 
before leaving this web site. 


<form onsubmit="encrypt();" action="http://formspree.io/drharbeck@gmail.com"
      method="post">
            <label>
                Your E-mail address <br>
                <textarea name="from" id="from" rows="1" cols="80"></textarea>
            </label> <br>
            <label>
                Message <br>
                <textarea name="message" id="message" cols="80" rows="10"></textarea>
            </label> <br>
            <button onlick="encrypt();">Send</button>
</form>







<script src="/static/js/openpgp.min.js"> </script>
<script>

function encrypt() {

   publicKeyString = "not tis";
   $.ajax({url:'/static/0BDD9EB4.asc', success: function(data){publicKeyString=data;},error: function(a,b,c) {window.alert (b);}, async:false});

   var pubkey = openpgp.key.readArmored(publicKeyString).keys;
 
   var options = {
    data: $('#from').val () + "\n" +$('#message').val(),       
    publicKeys: pubkey,
    armor: true
   };

    openpgp.encrypt(options).then(function(ciphertext) {
    encrypted = ciphertext.data; 
    $('#message').val (encrypted);
    $('#from').val ("hidden");
  });
}
</script>

