define([

], function (

) {
var getClickFeatureItem = null;
function getClickFeature(view,SimpleLineSymbol,Polyline,spatialReference,Graphic,Point,Polygon){
  getClickFeatureItem =view.on("click", function (event) {
        const pixelTolerance = 6;

        // 計算在當前比例尺下像素相當於多少地理距離
        const screenPoint1 = view.toMap({ x: event.x, y: event.y });
        const screenPoint2 = view.toMap({
          x: event.x + pixelTolerance,
          y: event.y,
        });

        const geodesicDistance = Math.sqrt(
          Math.pow(screenPoint1.x - screenPoint2.x, 2) +
            Math.pow(screenPoint1.y - screenPoint2.y, 2)
        );

        var currentScale = view.scale;
        view.graphics.removeAll(); // 移除現有標記

        var locationValue = `POINT(${event.mapPoint.x} ${event.mapPoint.y})`;
        console.log("選擇的坐標為:", locationValue);
        var data = {
          x: event.mapPoint.x,
          y: event.mapPoint.y,
          torelance: geodesicDistance,
        };

        var layerNum = 1;
        layer(data);

        // 獲取 CSRF token

        function getCsrfToken() {
          return document
            .querySelector('meta[name="csrf-token"]')
            .getAttribute("content");
        }

        // 全局設置 CSRF token，將其添加到所有 AJAX 請求的標頭中
        $.ajaxSetup({
          headers: {
            "X-CSRFToken": getCsrfToken(),
          },
        });
        //圖層1

        function layer(data) {
          $.ajax({
            type: "post",
            url: "/getfeature1/",
            data: data,
            headers: { "X-CSRFToken": getCsrfToken() }, // 添加 CSRF token
            dataType: "json",
            success: function (response) {
              if (!response.data || response.data.length === 0) {
                console.log("No data returned from the server");
                layer2(data);
                return;
              }

              var item = response.data[0].location_geojson;
              console.log(response.data[0].properties);
              var point = new Point({
                x: JSON.parse(item).coordinates[0],
                y: JSON.parse(item).coordinates[1],
                spatialReference: spatialReference,
              });

              var pointGraphic = new Graphic({
                geometry: point,
                symbol: markerSymbol2,
                attributes: response.data[0].properties, // 添加屬性
              });

              var popupPoint = new Point({
                x: event.mapPoint.x,
                y: event.mapPoint.y,
                spatialReference: spatialReference,
              });

              view.graphics.add(pointGraphic);

              // 彈窗
              view.popup.open({
                title: "我是點",
                content: `
              <b>名稱:</b> ${pointGraphic.attributes.name} <br>

          `,
                location: popupPoint,
              });
              view.popup.dockOptions.buttonEnabled = false;
            },
          });
        }

        //圖層2

        function layer2(data) {
          $.ajax({
            type: "post",
            url: "/getfeature2/",
            data: data,
            headers: { "X-CSRFToken": getCsrfToken() }, // 添加 CSRF token
            dataType: "json",
            success: function (response) {
              if (!response.data || response.data.length === 0) {
                console.log("No data returned from the server2");
                layerNum += 1;
                layer3(data);
                return;
              }

              var item = response.data[0].location_geojson;
              console.log(response.data[0].properties);

              var geoJson = JSON.parse(item);

              if (geoJson.type === "LineString") {
                var polyline = new Polyline({
                  paths: geoJson.coordinates,
                  spatialReference: spatialReference,
                });

                var lineGraphic = new Graphic({
                  geometry: polyline,
                  symbol: lineSymbol,
                  attributes: response.data[0].properties,
                });
                view.graphics.add(lineGraphic);

                var popupPoint = new Point({
                  x: event.mapPoint.x,
                  y: event.mapPoint.y,
                  spatialReference: spatialReference,
                });

                view.popup.open({
                  title: "我是線",
                  content: `<b>名稱:</b> ${lineGraphic.attributes.name} <br>`,
                  location: popupPoint,
                });
                view.popup.dockOptions.buttonEnabled = false;
              }
            },
          });
        }

        //圖層3
        function layer3(data) {
          $.ajax({
            type: "post",
            url: "/getfeature3/",
            data: data,
            headers: { "X-CSRFToken": getCsrfToken() }, // 添加 CSRF token
            dataType: "json",
            success: function (response) {
              if (!response.data || response.data.length === 0) {
                console.log("No data returned from the server3");
                layerNum += 1;
                return;
              }

              var item = response.data[0].location_geojson;
              console.log(response.data[0].properties);

              var geoJson = JSON.parse(item);
              console.log(geoJson.type);

              var polygon;

              if (geoJson.type === "Polygon") {
                polygon = new Polygon({
                  rings: geoJson.coordinates,
                  spatialReference: spatialReference,
                });
              } else if (geoJson.type === "MultiPolygon") {
                polygon = new Polygon({
                  rings: geoJson.coordinates.flat(1),
                  spatialReference: spatialReference,
                });
              } else {
                console.log("Unsupported geometry type: " + geoJson.type);
                return;
              }

              var polygonGraphic = new Graphic({
                geometry: polygon,
                symbol: polygonSymbol,
                attributes: response.data[0].properties,
              });
              view.graphics.add(polygonGraphic);

              var popupPoint = new Point({
                x: event.mapPoint.x,
                y: event.mapPoint.y,
                spatialReference: spatialReference,
              });

              view.popup.open({
                title: "我是面",
                content: `<b>名稱:</b> ${polygonGraphic.attributes.name} <br>`,
                location: popupPoint,
              });
              view.popup.dockOptions.buttonEnabled = false;
            },
          });
        }
        //
      });



      //樣式
      // 點擊事件，用於選擇位置
      var markerSymbol = {
        type: "simple-marker",
        color: "red",
        size: "12px",
        outline: {
          color: "black",
          width: 1,
        },
      };

      var markerSymbol2 = {
        type: "simple-marker",
        color: [0, 255, 255, 0.1],
        size: "12px",
        outline: {
          color: [0, 255, 255],
          width: 3,
        },
      };

      var lineSymbol = new SimpleLineSymbol({
        color: [0, 255, 255],
        width: 4,
      });

      let polygonSymbol = {
        type: "simple-fill",
        color: [0, 255, 255, 0.5],
        style: "solid",
        outline: {
          color: [0, 255, 255],
          width: 1,
        },
      };
      //
//
}


function disableClickEvent() {
    if (getClickFeatureItem) {
        getClickFeatureItem.remove();
    }}


  return {
    getClickFeature: getClickFeature,
    disableClickEvent:disableClickEvent
  };


})