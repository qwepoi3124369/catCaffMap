

require([
  "esri/Map",
  "esri/views/MapView",
  "esri/layers/WMSLayer",
  "esri/geometry/SpatialReference",
  "esri/geometry/Extent",
  "esri/widgets/ScaleBar",
  "esri/Graphic",
  "esri/geometry/Point",
  "esri/config", // 加載 config 模塊
  "esri/layers/GeoJSONLayer",
  "esri/symbols/SimpleLineSymbol",
    "esri/symbols/TextSymbol",
  "esri/Color",
  "esri/geometry/Polyline",
  "esri/geometry/Polygon",
  "esri/symbols/SimpleFillSymbol",
  "esri/geometry/Circle",
  "esri/layers/GraphicsLayer",
      "esri/symbols/PictureMarkerSymbol",
      "esri/layers/FeatureLayer",
  "/static/mapjs/getClickFeature.js",
   "/static/mapjs/buffer.js",
   "/static/mapjs/atrributeSearch.js"
], function (
  Map,
  MapView,
  WMSLayer,
  SpatialReference,
  Extent,
  ScaleBar,
  Graphic,
  Point,
  esriConfig,
  GeoJSONLayer,
  SimpleLineSymbol,
  TextSymbol,
  Color,
  Polyline,
  Polygon,
  SimpleFillSymbol,
  Circle,
  GraphicsLayer,
  PictureMarkerSymbol,
  FeatureLayer,
  getClickFeature,
  bufferStart,
  atrributeSearchStart
){




  var twd97 = new SpatialReference({ wkid: 3826 });

  // 初始化地圖範圍
  var initialExtent = new Extent({
    xmin: 165335.590272,
    ymin: 2485542.346555,
    xmax: 255014.164917,
    ymax: 2596519.275360,
    spatialReference: twd97,
  });

  // 創建地圖對象
  var map = new Map({ basemap: null });

  // 初始化 MapView
  var view = new MapView({
    container: "map",
    map: map,
    extent: initialExtent,
    spatialReference: twd97,
    logo: false,
    constraints: {
      maxScale: 5000,
      minScale: 2700000,
    },
  });

  // 底圖
  var wmsLayer = new WMSLayer({
    url: "https://wms.nlsc.gov.tw/wms",
    sublayers: [
      {
        name: "EMAP6",
        title: "臺灣通用電子地圖透明",
      },
    ],
    opacity: 1.0,
    visible: true,
  });

  // 將 WMS 圖層添加到地圖
    map.add(wmsLayer);


//let catCafeLayer=new GraphicsLayer()
//  map.add(catCafeLayer);
//
////    var markerSymbol = {
////             type: "simple-marker",
////             color: "red",
////             size: "12px",
////             outline: {
////                 color: "black",
////                 width: 1
////             }
////         };
//             var markerSymbol = new PictureMarkerSymbol({
//  url:staticBaseUrl + 'images/cat.png', // 使用 Django 的静态文件路径
//  width: "28px",
//  height: "36px",
//  yoffset: 16, // 垂直偏移量，将图标底部对齐到点位置（高度的一半）
//  anchor: "bottom" ,// 锚点设置为底部
//
//});
//
//catCafe.features.forEach(feature => {
//   console.log(feature);
//
//var point = new Point({
//                x: JSON.parse(feature.geometry).coordinates[0],
//                y: JSON.parse(feature.geometry).coordinates[1],
//                spatialReference: twd97
//            });
//
//            var pointGraphic = new Graphic({
//                geometry: point,
//                symbol: markerSymbol,
//
//
//                  popupTemplate: {
//                        title: "名稱:"+feature.properties.name,
//                        content: "地址: {address} <br> 評分: {rating} <br> <a href='https://www.youtube.com/'>ddd</a>"
//                    }
//            });
//
//
//
//
//
//            catCafeLayer.add(pointGraphic);
//
//        });

// 1. 定義聚類符號
//var markerSymbol = new PictureMarkerSymbol({
//  url: staticBaseUrl + 'images/cat.png', // 使用 Django 的静态文件路径
//  width: "28px",
//  height: "36px",
//  yoffset: 16, // 垂直偏移量，将图标底部对齐到点位置（高度的一半）
//  anchor: "bottom" // 锚点设置为底部
//});

let mylayer= {};




let polygonSymbol = {
        type: "simple-fill",
        color: [0, 255, 255, 0.1],
        style: "solid",
        outline: {
          color: [0, 0, 0],
          width: 2,
        },
      };

 let kaohsiungLayer=new GraphicsLayer()
 map.add(kaohsiungLayer)
mylayer["kaohsiungLayer"] = kaohsiungLayer;


kaohsiung.features.forEach(feature => {
 var polygonGeometry

           if (JSON.parse(feature.geometry).type === "Polygon") {
                polygonGeometry = new Polygon({
                  rings: JSON.parse(feature.geometry).coordinates,
                  spatialReference: twd97,
                });
              } else if (JSON.parse(feature.geometry).type === "MultiPolygon") {
                polygonGeometry = new Polygon({
                  rings: JSON.parse(feature.geometry).coordinates.flat(1),
                  spatialReference: twd97,
                });
              } else {
                console.log("錯誤為: " + JSON.parse(feature.geometry).type);
                return;
              }

     var polygonGraphic = new Graphic({
    geometry: polygonGeometry,
    symbol: polygonSymbol,
    attributes: feature.properties, // 保留原始屬性
    //       popupTemplate: {
    //                        title: "名稱:"+feature.properties.name,
    //                        content: "{name}"
    //                  }
  });

  // 創建標籤（TextSymbol）
// 創建標籤（TextSymbol）
var labelSymbol = new TextSymbol({
  text: feature.properties.name,  // 標籤顯示的內容
  font: {
    size: 8,
//    family: "Arial",  // 使用 Arial 作為字體
//    weight: "bold"    // 設置字體為粗體
  },
  color: "black", // 標籤顏色
  haloColor: "white", // 標籤邊緣的顏色
  haloSize: 2 // 邊緣的寬度
});

// 創建一個標籤圖形，將標籤放置在多邊形的中心
var labelGraphic = new Graphic({
  geometry: polygonGeometry.centroid, // 標籤放在多邊形的中心
  symbol: labelSymbol,
  attributes: feature.properties
});
kaohsiungLayer.add(polygonGraphic);
kaohsiungLayer.add(labelGraphic);

// 檢查地圖的比例尺，並根據比例尺來調整標籤顯示
})



//

//叢集圖
let markerSymbol = {
  type: "simple-marker",
  color: [0, 0, 255], // 藍色
  size: "12px",
  outline: {
    color: [0, 0, 0], // 白色邊框
    width: 2
  }
};
var clusterSymbol = {
  type: "simple-marker",
  color: [255, 0, 0], // 聚類顏色（紅色）
  size: "24px", // 聚類圖形大小
  outline: {
    color: [255, 255, 255], // 外圍邊框顏色（白色）
    width: 2
  }
  }

var labelingInfo = [
  {
    labelExpressionInfo: {
      expression: "$feature.cluster_count" // 顯示聚類內點的數量
    },
    symbol: {
      type: "text", // 顯示為文本
      color: [255, 255, 255], // 文字顏色（白色）
      font: {
        size: 12, // 字體大小
        weight: "bold"
      }
    },
    labelPlacement: "center-center" // 標籤顯示在圖形中心
  }
];

var currentUrl = window.location.href;

// 2. 定義聚類圖層
var clusterLayer = new FeatureLayer({
  source: [],  // 用來儲存圖徵的資料
  spatialReference: twd97,
  objectIdField: "id",
  geometryType: "point",
  fields: [
    { name: "id", type: "oid" },
    { name: "name", type: "string" },
    { name: "address", type: "string" },
    { name: "type", type: "string" },
       { name: "rate", type: "string" }
  ],
  popupTemplate: {
    title: "{name}",
    content: `    <div>
      <p>地址: {address}</p>
      <p>貓咪種類: {type}</p>
      <p>評分: {rate}星</p>
      <div class="d-flex align-items-center justify-content-center ">
      <a href="${currentUrl}catCafeDetail/{id}" class='mx-auto btn btn-danger text-white moreCafe' target="_blank"     data-id="{id}">更多資訊</a>
        </div>
    </div>`
  },

  featureReduction: {
     type: "cluster", // 啟用聚類
    clusterRadius: "160px", // 聚類半徑
    clusterMinSize: "24px", // 聚類最小大小
    clusterMaxSize: "40px", // 聚類最大大小
    symbol: clusterSymbol, // 聚類符號
 labelingInfo:labelingInfo
  },
   renderer: {
    type: "simple",
    symbol: markerSymbol
  }
});


map.add(clusterLayer);
mylayer["clusterLayer"] = clusterLayer;

catCafe.features.forEach(feature => {
  var point = new Point({
    x: JSON.parse(feature.geometry).coordinates[0],
    y: JSON.parse(feature.geometry).coordinates[1],
    spatialReference: twd97
  });

  var pointGraphic = new Graphic({
    geometry: point,
//    symbol: markerSymbol,
    attributes: feature.properties // 保留原始屬性
  });

  clusterLayer.source.add(pointGraphic); // 將圖徵添加到聚類圖層
})



//





//  var wmsLayer4 = new WMSLayer({
//    url: "http://localhost:8080/geoserver/geodjango/wms",
//    sublayers: [
//      {
//        name: "geologmap",
//        title: "geologmap",
//      },
//    ],
//    opacity: 1.0,
//    visible: true,
//  });
//
//  // 將 WMS 圖層添加到地圖
//  map.add(wmsLayer4);

//  var wmsLayer3 = new WMSLayer({
//    url: "/geoserver/geodjango/wms",
//    sublayers: [
//      {
//        name: "world_line",
//        title: "world_line",
//      },
//    ],
//    opacity: 1.0,
//    visible: true,
//  });
//
//  // 將 WMS 圖層添加到地圖
//  map.add(wmsLayer3);
//
//  var wmsLayer2 = new WMSLayer({
//    url: "/geoserver/geodjango/wms",
//    sublayers: [
//      {
//        name: "world_house",
//        title: "world_house",
//      },
//    ],
//    opacity: 1.0,
//    visible: true,
//  });
//
//  // 將 WMS 圖層添加到地圖
//  map.add(wmsLayer2);

//getClickFeature.getClickFeature(view,SimpleLineSymbol,Polyline,twd97,Graphic,Point,Polygon )
//  getClickFeature();

  // 比例尺
  var scalebar = new ScaleBar({ view: view, unit: "metric" });
  view.ui.add(scalebar, { position: "bottom-left" });

bufferStart.bufferStart(view,GraphicsLayer,map,clusterLayer,Point,Circle,Graphic,twd97)
atrributeSearchStart.atrributeSearchStart(view,initialExtent,clusterLayer,GraphicsLayer,map,Point,twd97,Graphic)

function changeLayerOrder(layer, index) {
  map.layers.reorder(layer, index);
}
let myLayerOrder=['kaohsiungLayer', 'clusterLayer']
            $("#sortable").sortable({
                update: function(event, ui) {
                    var newOrder = $(this).sortable('toArray', {attribute: 'id'});
                    let newOrderNum=newOrder.length
                    console.log(newOrderNum)
                    for(let i=0;i<newOrderNum;i+=1){

                    changeLayerOrder(mylayer[newOrder[i]] , -(i-newOrderNum))
                    console.log(newOrder[i])
                    console.log(-(i-newOrderNum-1))
                    myLayerOrder=newOrder
                  }
                }
            });
            $("#sortable").disableSelection();





  document.getElementById('toggleWmsLayer2').addEventListener('change', function() {
  var layerVisible = this.checked;  // 当checkbox被选中时，layerVisible为true，否则为false
  if(layerVisible){
    clusterLayer.visible = !clusterLayer.visible;
  }
  else{
    clusterLayer.visible = !clusterLayer.visible;
  }

})



document.getElementById('toggleWmsLayer3').addEventListener('change', function() {
  var layerVisible = this.checked;  // 当checkbox被选中时，layerVisible为true，否则为false
  if(layerVisible){
    kaohsiungLayer.visible = !kaohsiungLayer.visible;
  }
  else{
    kaohsiungLayer.visible = !kaohsiungLayer.visible;
  }

})



//dqw
});
