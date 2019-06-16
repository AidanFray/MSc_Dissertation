function doGet(e) {
  var form = FormApp.openById('14h2xS2iWBYhWsj41x9rW-pbxYPtl3sYHnQxjRB5-YpQ')
  var ss = SpreadsheetApp.getActive();
  
  //ScriptApp.newTrigger('onFormSubmit').forForm(form).onFormSubmit().create();
  
  setUpForm_(ss, form);
  return ContentService.createTextOutput("OK").setMimeType(ContentService.MimeType.TEXT);
}

function setUpForm_(ss, form) {
  // Create the form and add a multiple-choice question for each timeslot.  
  
  var min_num_per_section = 5;
  var algos = ["Soundex", "Metaphone", "Leven", "NYSIIS", "WordVec", "Random"];
  var algos_sizes = [763777, 412916, 97730, 188474, 14550, 10000];
  
  //init_form(form, algos, min_num_per_section);
  
  formItems = form.getItems();
  
  // Updates the new values
  var algo_index = 0;
  var scale_index = 0;
  for (var i = 0; i < formItems.length; i++)
  {
    if (formItems[i].getType() == "SCALE")
    {
      var rnd_index = Math.floor(Math.random() * algos_sizes[algo_index]) + 1;    
      
      var sheetname = algos[algo_index];
      var sheet = ss.getSheetByName(sheetname);
      var range = sheet.getRange(rnd_index, 1)
      var values = range.getValues();
           
      _updateScaleTitle(formItems[i], values[0]);
      
      scale_index++;
      
      // Dynamically groups
      if (scale_index != 0)
      {
        if (scale_index % min_num_per_section == 0) algo_index++;
      }
    }
  }
}

function init_form(form, algos, min_num_per_section) 
{ 
  form.addPageBreakItem();
  
  for(var i = 0; i < algos.length; i++)
  {
    //form.addPageBreakItem().setTitle(algos[i]);
    
    for(var x = 0; x < min_num_per_section; x++)
    {
      _addScale(form, 'X');
    }
  }
}

function _addScale(form, string){
  var item = form.addScaleItem();
  item.setTitle(string);
  item.setBounds(1, 5);
  item.setLabels("Very different sound", "Very similar sound");
}

function _updateScaleTitle(item, string) {
  item.setTitle(string);
}

function onFormSubmit(e) {
  doGet(e);
}