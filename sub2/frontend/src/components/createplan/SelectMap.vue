<template>
  <div class="map_wrap">
    <div id="map" style="width:100%;height:100%;position:relative;overflow:hidden;"></div> 
    
    <div class="custom_typecontrol radius_border">
        <span id="btnRoadmap" class="selected_btn" @click="setMapType('roadmap')">지도</span>
        <span id="btnSkyview" class="btn" @click="setMapType('skyview')">스카이뷰</span>
    </div>
    
    <div class="custom_zoomcontrol radius_border"> 
        <span @click="zoomIn()">
          <img src="https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/ico_plus.png" alt="확대">
        </span>  
        <span @click="zoomOut()">
            <img src="https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/ico_minus.png" alt="축소">
        </span>
    </div>
  </div>
  
</template>

<script>
import cities from '../../../public/city.json'

export default {
    name: 'dmap',
    props:{
        destinations:{
            type:Array,
            required:true
        }
    },
    data() {
        return {
            map:null,
        }
    },
    mounted() {
      this.mapSetting()
    },
    methods:{
        mapSetting(){
            var container = document.getElementById('map');
            var mapOptions = {
                center: new kakao.maps.LatLng(35.850701, 127.570667),
                level: 13 //지도의 레벨(확대, 축소 정도)
            }
            this.map = new kakao.maps.Map(container, mapOptions)
            var map = this.map
            var clusterer = new kakao.maps.MarkerClusterer({
                map: map, // 마커들을 클러스터로 관리하고 표시할 지도 객체 
                averageCenter: true, // 클러스터에 포함된 마커들의 평균 위치를 클러스터 마커 위치로 설정 
                minLevel: 10 // 클러스터 할 최소 지도 레벨 
            })
            var markers = []
            for (var i = 0; i < cities.length; i ++) {
                // 마커를 생성합니다
                var marker = new kakao.maps.Marker({
                    map: map, // 마커를 표시할 지도
                    position: new kakao.maps.LatLng(cities[i].longitude, cities[i].latitude), // 마커의 위치
                });

                // 마커에 표시할 인포윈도우를 생성합니다 
                var infowindow = new kakao.maps.InfoWindow({
                    content: cities[i].cityName // 인포윈도우에 표시할 내용
                });
                kakao.maps.event.addListener(marker, 'mouseover', this.makeOverListener(map, marker, infowindow));
                kakao.maps.event.addListener(marker, 'mouseout', this.makeOutListener(infowindow));
                kakao.maps.event.addListener(marker, 'click', this.makeClickListener(marker, infowindow, this.destinations))
                markers.push(marker)
            }
            clusterer.addMarkers(markers);
        },
        setMapType(maptype) {
            var map = this.map
            var roadmapControl = document.getElementById('btnRoadmap');
            var skyviewControl = document.getElementById('btnSkyview');
            if (maptype === 'roadmap') {
                map.setMapTypeId(kakao.maps.MapTypeId.ROADMAP)
                roadmapControl.className = 'selected_btn'
                skyviewControl.className = 'btn'
                }
            else {
                map.setMapTypeId(kakao.maps.MapTypeId.HYBRID)
                skyviewControl.className = 'selected_btn'
                roadmapControl.className = 'btn'
            }
        },
        zoomIn() {
            var map = this.map
            map.setLevel(map.getLevel() - 1)
        },
        zoomOut() {
            var map = this.map
            map.setLevel(map.getLevel() + 1)
        },
        makeOverListener(map, marker, infowindow) {
            return function() {
                infowindow.open(map, marker)
            }
        },
        makeOutListener(infowindow) {
            return function() {
                infowindow.close()
            }
        },
        makeClickListener(marker, infowindow, destinations){
            return function() {
                // console.log(destinations)
                var flag = true
                for (var i=0; i < destinations.length; i++){
                    if (destinations[i][0].getPosition().equals(marker.getPosition())){
                        destinations.splice(i,1)
                        flag = false
                        break
                    }
                }
                if (flag){
                    destinations.push([marker, infowindow.getContent()])
                }
            }
        }
    },
}
</script>

<style>
.map_wrap {position:relative;overflow:hidden;width:100%;height:800px;}
.radius_border{border:1px solid #919191;border-radius:5px;}     
.custom_typecontrol {position:absolute;top:10px;right:10px;overflow:hidden;width:130px;height:30px;margin:0;padding:0;z-index:1;font-size:12px;font-family:'Malgun Gothic', '맑은 고딕', sans-serif;}
.custom_typecontrol span {display:block;width:64px;height:30px;float:left;text-align:center;line-height:30px;cursor:pointer;}
.custom_typecontrol .btn {background:#fff;background:linear-gradient(#fff,  #e6e6e6);}       
.custom_typecontrol .btn:hover {background:#f5f5f5;background:linear-gradient(#f5f5f5,#e3e3e3);}
.custom_typecontrol .btn:active {background:#e6e6e6;background:linear-gradient(#e6e6e6, #fff);}    
.custom_typecontrol .selected_btn {color:#fff;background:#425470;background:linear-gradient(#425470, #5b6d8a);}
.custom_typecontrol .selected_btn:hover {color:#fff;}   
.custom_zoomcontrol {position:absolute;top:50px;right:10px;width:36px;height:80px;overflow:hidden;z-index:1;background-color:#f5f5f5;} 
.custom_zoomcontrol span {display:block;width:36px;height:40px;text-align:center;cursor:pointer;}     
.custom_zoomcontrol span img {width:15px;height:16px;margin:12px 0;border:none;}             
.custom_zoomcontrol span:first-child{border-bottom:1px solid #bfbfbf;} 
</style>