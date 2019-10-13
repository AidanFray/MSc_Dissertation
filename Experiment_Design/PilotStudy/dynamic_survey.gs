var FORM_ID = "14h2xS2iWBYhWsj41x9rW-pbxYPtl3sYHnQxjRB5-YpQ";

var ALGOS =       ["Soundex", "Metaphone", "Leven", "NYSIIS", "WordVec", "Random"];
var ALGO_SIZES =  [763777,     412916,      97730,   188474,   73962,     10000];

var QUESTION_PER_ALGO = 5;

function doGet(e) {
  var form = FormApp.openById(FORM_ID);
  var ss = SpreadsheetApp.getActive();
  
  updateForm(ss, form);
  return ContentService.createTextOutput("OK").setMimeType(ContentService.MimeType.TEXT);
}

function addSubmitTrigger() {
  var form = FormApp.openById(FORM_ID);
  ScriptApp.newTrigger('onFormSubmit').forForm(form).onFormSubmit().create();
}

function initForm() {
  var form = FormApp.openById(FORM_ID);
  var ss = SpreadsheetApp.getActive();
  
  form.addPageBreakItem();
  
  for(var i = 0; i < ALGOS.length; i++)
  {    
    for(var x = 0; x < QUESTION_PER_ALGO; x++)
    {
      _addScale(form, 'X');
    }
  }
  
  updateForm(ss, form);
}

function updateForm(ss, form) {
  formItems = form.getItems();
  
  // Updates the new values
  var algo_index = 0;
  var scale_index = 0;
  for (var i = 0; i < formItems.length; i++)
  {
    if (formItems[i].getType() == "SCALE")
    {
      // Ignores the scale for Engligh comprehension
      if (formItems[i].getTitle() == "English comprehension") continue;
      
      // Ignores the atension questions
      if (formItems[i].getTitle() == "UNIVERSITY-UNIVERSITY") continue;
      if (formItems[i].getTitle() == "DYNAMIC-DYNAMIC") continue;
      
      var rnd_index = Math.floor(Math.random() * ALGO_SIZES[algo_index]) + 1;    
      
      var sheetname = ALGOS[algo_index];
      var sheet = ss.getSheetByName(sheetname);
      var range = sheet.getRange(rnd_index, 1)
      var values = range.getValues();
           
      _updateScaleTitle(formItems[i], values[0]);
      
      scale_index++;
      
      // Dynamically groups
      if (scale_index != 0)
      {
        if (scale_index % QUESTION_PER_ALGO == 0) algo_index++;
      }
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