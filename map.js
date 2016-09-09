function main() {
  // Initialize map centered on my hometown.
  var map = L.map('map', {
    doubleClickZoom: false,
    layers: [L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png')],
    center: [48.49, 1.395],
    zoom: 16
  });

  // Pusher credentials
  var pusher_key = '01a9feaaf9ebb120d1a6';

  // Mozilla demo server (flushed every day)
  var server = "https://kinto.dev.mozaws.net/v1";
  // Simplest credentials ever.
  var headers = {Authorization: "Basic " + btoa("token:your-own-secret")};

  // The "default" bucket is handy because it does not have
  // to be created.
  var bucket = "default";
  // Arbitrary collection id.
  var collection_id = "kinto_demo_leaflet";
  // Kinto client.
  var kinto = new KintoClient(server, {headers: headers});
  var client = kinto.bucket(bucket)
                    .collection(collection_id);

  // Global to associate map markers with record ids.
  var markers = {};

  // Setup live sync.
  getBucketId()
    .then(setupLiveSync);

  // Load previously created records.
  client.listRecords()
    .then(function(results) {
      // Add each marker to map.
      results.data.map(addMarker);
    });

  // Create marker on double-click.
  map.on('dblclick', function(event) {
    // Save on server... marker will be added to map
    // when pusher event is received.
    // (enough for demo, but bad for UX)
    client.createRecord({latlng: event.latlng});
  });

  function addMarker(record) {
    // Create new map marker.
    var marker = L.marker(record.latlng, {draggable: true})
                  .addTo(map);
    // Store reference by record id.
    markers[record.id] = marker;

    // Listen to events on marker.
    marker.on('click', function () {
      client.deleteRecord(record.id);
    });
    marker.on('dragend', function () {
      var updated = Object.assign({}, record, {latlng: marker.getLatLng()});
      client.updateRecord(updated);
    });
  }

  function removeMarker(record) {
    map.removeLayer(markers[record.id]);
    delete markers[record.id];
  }

  function getBucketId() {
    // When using the `default` bucket, we should resolve its real id
    // to be able to listen to notifications.
    if (bucket != "default")
      return Promise.resolve(bucket);

    return kinto.fetchServerInfo()
      .then(function (result) {
        return result.user.bucket;
    });
  }

  function setupLiveSync(bucket_id) {
    var pusher = new Pusher(pusher_key, {
      encrypted: true
    });

    // The channel name. It should match the setting
    // `kinto.event_listeners.pusher.channel`
    var channelName = bucket_id + '-' + collection_id + '-record';

    var channel = pusher.subscribe(channelName);
    channel.bind('create', function(data) {
      data.map(function (change) {
        addMarker(change.new);
      });
    });
    channel.bind('update', function(data) {
      data.map(function (change) {
        markers[change.new.id].setLatLng(change.new.latlng);
      });
    });
    channel.bind('delete', function(data) {
      data.map(function (change) {
        removeMarker.bind(change.old);
      });
    });
  }
}

window.addEventListener("DOMContentLoaded", main);





// https://jsbin.com/cebubopiye/1/edit?js,output
// https://jsbin.com/yewipufofo/6/edit?html,js
// https://jsbin.com/qikujegili/4/edit?html,css,js,output
