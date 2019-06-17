function doGet(e) {
  var form = FormApp.openById('')
  var ss = SpreadsheetApp.getActive();
  
  //ScriptApp.newTrigger('onFormSubmit').forForm(form).onFormSubmit().create();
  
  setUpForm_(ss, form);
  return ContentService.createTextOutput("OK").setMimeType(ContentService.MimeType.TEXT);
}

function setUpForm_(ss, form) {
  // Create the form and add a multiple-choice question for each timeslot.  
  
  var min_num_per_section = 5;
  var algos = ["Soundex", "Metaphone"];
  
  //init_form(form, algos, min_num_per_section);
  
  formItems = form.getItems();
  
  // Updates the new values
  var algo_index = 0;
  var scale_index = 0;
  for (var i = 0; i < formItems.length; i++)
  {
    if (formItems[i].getType() == "SCALE")
    {
      var sheetname = algos[algo_index];
      var sheet = ss.getSheetByName(sheetname);
      var range = sheet.getDataRange();
      var values = range.getValues();
      
      var rnd_index = Math.floor(Math.random() * values.length - 1) + 1;
      _updateScaleTitle(formItems[i], values[rnd_index]);
      
      scale_index++;
      
      // Dynamically groups
      if (scale_index != 0)
      {
        if (scale_index % min_num_per_section == 0) algo_index++;
      }
    }
  }
}

function init_form(form, algos, min_num_per_section) {
 
  // Description  
  form.addSectionHeaderItem().setTitle("For each question below, please rate how similar each pair SOUNDS to one another on a scale of 1 to 5. When comparing the words please sound out each word.");
  form.addSectionHeaderItem().setTitle("If you're not sure on the correct pronunciation please leave the question unanswered.");
  
  form.addPageBreakItem().setTitle("Demographic");
  //TODO: Add demographical question
  
  for(var i = 0; i < algos.length; i++)
  {
    form.addPageBreakItem().setTitle(algos[i]);
    
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