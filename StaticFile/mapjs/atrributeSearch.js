define([

], function (
) {
//
let catCafeLayer
let SelectLayer
let AttributeData
var currentUrl = window.location.href;
function atrributeSearchStart(view,initialExtent,clusterLayer,GraphicsLayer,map,Point,twd97,Graphic){
$("#stopAtrributeSearch").click(function(){
$("#mapButton").hide()
$("#FunctionButtons").show()
$("#atrributeSearchButton").hide()
clusterLayer.visible=true
map.remove(catCafeLayer); // 從地圖中移除 catCafeLayer
map.remove(SelectLayer);
closeMapDialog()

})

$("#restrartAtrributeSearch").click(function(){
$("#mapButton").hide()
$("#FunctionButtons").show()
$("#atrributeSearchButton").hide()
clusterLayer.visible=true
map.remove(catCafeLayer);
map.remove(SelectLayer);
openMapDialog();
showAnalysis()
})




$("#Searchattribute").click(function(){
if($("#maxRateAttribute").val()>=$("#minRateAttribute").val())
{
view.goTo(initialExtent);
closeMapDialog()
clusterLayer.visible=false
AttributeData={
name:$("#nameAttribute").val(),
type:$("#typeAttribute").val(),
district:$("#districtAttribute").val(),
minRate:$("#minRateAttribute").val(),
maxRate:$("#maxRateAttribute").val(),
page:1
}
console.log(AttributeData)
 $.ajax({
        type: "post",
        url: "/attributeSearch/",
        data: AttributeData,
        headers: { "X-CSRFToken": getCsrfToken() }, // 添加 CSRF token
        dataType: "json",
        success: function (response) {
   console.log(response.pagesNum)
         $("#dataList").html("")
 $("#SearchDatapage").html("")
  searchDataType="attributeSearch"
  for(let i= 1;i<=response.pagesNum;i++){
 $("#SearchDatapage").append(`
   <option value=${i}>第${i}頁</option>
 `)
  }

    catCafeLayer=new GraphicsLayer()
  map.add(catCafeLayer);

    var catCafeLayerSymbol = {
             type: "simple-marker",
             color: "red",
             size: "12px",
             outline: {
                 color: "black",
                 width: 1
             }
         };



      response.allData.forEach((data, index) => {
     let point = new Point({
                x: JSON.parse(data.location_geojson).coordinates[0],
                y: JSON.parse(data.location_geojson).coordinates[1],
                spatialReference: twd97
            });

            let pointGraphic = new Graphic({
                geometry: point,
                symbol: catCafeLayerSymbol,
                  popupTemplate: {
                        title: data.properties.name,
                        content:
                         `    <div>
      <p>地址: ${data.properties.address}</p>
      <p>貓咪種類: ${data.properties.type}</p>
      <p>評分: ${data.properties.rate}星</p>
      <div class="d-flex align-items-center justify-content-center ">
      <a href="${currentUrl}catCafeDetail/${data.properties.id}" class='mx-auto btn btn-danger text-white moreCafe' target="_blank"     data-id="{id}">更多資訊</a>
        </div>
    </div>`

                    }
            });

            catCafeLayer.add(pointGraphic);

      })

      CreateSearchData(response)







$("#atrributeSearchButton").show()
$("#mapButton").show()
$("#FunctionButtons").hide()
console.log(response)
        }
        })
}else{
alert("最大價格應大於等於最小價格")
}

})
//asd
 function CreateSearchData(response){
let nowpage = parseInt($("#SearchDatapage").val());

if(response.allData.length==0){
  $("#dataList").append(
`<tr id="searchNoData">
    <td>查無資料</td>
</tr>`
  )
}
       response.data.forEach((data, index) => {
       let num=(index+1)+((nowpage-1)*3)
       let jsonString = JSON.stringify(data.properties);  // 將物件轉換為 JSON 字串
     console.log(jsonString)
       $("#dataList").append(
       `
         <tr style="height:20% width:100%" >
             <td  style="width:15% ;vertical-align: middle;" class="text-center">${num}</td>
             <td style="width:30% ;vertical-align: middle;" class="text-center"> ${data.properties.name}</td>
                <td class=" text-center mx-0" style="width:50%">
                        <button value='${data.location_geojson}' data-attribute='${jsonString}' class=" mx-1 my-1 btn btn-danger col-7 col-lg-4 zoomInGeojSON">縮放至</button>
                    <a href="${currentUrl}catCafeDetail/${data.properties.id}" class="mx-1 my-1 btn btn-danger col-7 col-lg-5" target="_blank">詳細資訊</a>
                    </td>

//
          </tr>



       `
       )

          $(".zoomInGeojSON").click(function(){
    map.remove(SelectLayer)
    SelectLayer=new GraphicsLayer()
    map.add(SelectLayer)
        let geoJsonData = JSON.parse($(this).val()); // jQuery 會自動解析 JSON
          let attribute = JSON.parse(this.dataset.attribute);  // 讀取 data-lon
          console.log(attribute.id)
        let x=geoJsonData.coordinates[0]
        let y=geoJsonData.coordinates[1]
         let point = new Point({
      x: x,  // TWD97 X (經度)
      y: y,  // TWD97 Y (緯度)
      spatialReference: twd97 // TWD97 WKID
    });
let BuffermarkerSymbol= {
             type: "simple-marker",
             color:  [0, 0, 0, 0],
             size: "12px",
             outline: {
                 color: "blue",
                 width: 3
             }
         };
         var currentUrl = window.location.href;
        let selectPointGraphic = new Graphic({
                geometry: point,
                symbol: BuffermarkerSymbol,
                  popupTemplate: {
                        title: attribute.name,
                        content:
                                      `    <div>
      <p>地址: ${attribute.address}</p>
      <p>貓咪種類: ${attribute.type}</p>
      <p>評分: ${attribute.rate}星</p>
      <div class="d-flex align-items-center justify-content-center ">
      <a href="${currentUrl}catCafeDetail/${attribute.id}" class='mx-auto btn btn-danger text-white moreCafe' target="_blank"     data-id="{id}">更多資訊</a>
        </div>
    </div>`

                    }
            });

            SelectLayer.add(selectPointGraphic);
view.popupEnabled = true;
view.popup.open({
    features: [selectPointGraphic], // 設定 popup 的內容來自這個圖徵
    location: point // 設定 popup 位置
});


    view.goTo({
      target: point,  // 使用 TWD97 座標
       scale: 5000     // 設定比例尺為 1:5000
    })

    if (window.innerWidth <992) {
closeMapDialog()
}

});

    console.log(`Index: ${index} Name: ${data.properties.name}`);
});

      }


      $("#SearchDatapage").change(function(){
let changePage= $("#SearchDatapage").val()
if(searchDataType=="attributeSearch"){
AttributeData.page = changePage
  $.ajax({
        type: "post",
        url: "/attributeSearch/",
        data: AttributeData,
        headers: { "X-CSRFToken": getCsrfToken() }, // 添加 CSRF token
        dataType: "json",
        success: function (response) {
         $("#dataList").html("")
 CreateSearchData(response)
        }
})
}

})

}
//
 return {
    atrributeSearchStart: atrributeSearchStart,
  };
})