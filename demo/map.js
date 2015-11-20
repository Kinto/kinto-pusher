function main() {
  // Mozilla demo server (flushed every day)
  var server = "http://localhost:8888/v1";
  // Simplest credentials ever.
  var headers = {Authorization: "Basic " + btoa("public:notsecret")};
  // Default bucket.
  var bucket = "default";
  // Arbitrary collection id.
  var collection_id = "kinto_demo_leaflet";

  // Pusher credentials
  var pusher_key = '01a9feaaf9ebb120d1a6';

  // Kinto client with sync options.
  var kinto = new Kinto({bucket: bucket, remote: server, headers: headers});

  // Local store in IndexedDB.
  var store = kinto.collection(collection_id);

  // Initialize map centered on my hometown.
  var map = L.map('map', {
    doubleClickZoom: false,
    layers: [L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png')],
    center: [48.49, 1.395],
    zoom: 16
  });

  // Group of markers.
  var markers = {};

  // Load previously created records.
  store.list()
    .then(function(results) {
      // Add each marker to map.
      results.data.map(addMarker);
    })
    .then(syncServer);

  // Create marker on double-click.
  map.on('dblclick', function(event) {
    // Save in local store.
    store.create({latlng: event.latlng})
      .then(function (result) {
        // Add marker to map.
        addMarker(result.data);
      })
      .then(syncServer);
  });

  // Setup live-sync!
  getBucketId()
   .then(setupLiveSync);


  function addMarker(record) {
    // Create new marker.
    var marker = L.marker(record.latlng, {draggable: true})
                  .addTo(map);
    // Store reference by record id.
    markers[record.id] = marker;

    // Listen to events on marker.
    marker.on('click', function () {
      store.delete(record.id)
        .then(removeMarker.bind(undefined, record))
        .then(syncServer);
    });
    marker.on('dragend', function () {
      record.latlng = marker.getLatLng();
      store.update(record)
        .then(syncServer);
    });
  }

  function removeMarker(record) {
    map.removeLayer(markers[record.id]);
    delete markers[record.id];
  }

  function syncServer() {
    var options = {strategy: Kinto.syncStrategy.CLIENT_WINS};
    store.sync(options)
      .then(function (result) {
        if (result.ok) {
          // Add markers for newly created records.
          result.created.map(addMarker);
          // Remove markers of deleted records.
          result.deleted.map(removeMarker);
        }
      })
      .catch(function (err) {
        // Special treatment since the demo server is flushed.
        if (/flushed/.test(err.message)) {
          // Mark every local record as «new» and re-upload.
          return store.resetSyncStatus()
            .then(syncServer);
        }
        throw err;
      });
  }

  function getBucketId() {
    // When using the `default` bucket, we should resolve its real id
    // to be able to listen to notifications.
    if (bucket != "default")
      return Promise.resolve(bucket);

    return fetch(server + '/buckets/' + bucket, {headers: headers})
      .then(function (result) {
        return result.json();
      })
      .then(function (result) {
        return result.data.id;
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
        if (markers[change.new.id])
          return; // Ignore our own events.

        // Store as if it was synced, and add to map.
        store.create(change.new, {synced: true})
          .then(addMarker.bind(undefined, change.new));
      });
    });
    channel.bind('update', function(data) {
      data.map(function (change) {
        // If local modification exists, ignore remote modification.
        store.get(change.old.id)
         .then(function (existing) {
           if (existing.data._status != 'synced')
             return;
           // Store locally as if it was synced.
           store.update(change.new, {synced: true})
             .then(function (result) {
                markers[result.data.id].setLatLng(change.new.latlng);
             });
         });
      });
    });
    channel.bind('delete', function(data) {
      data.map(function (change) {
        if (!markers[change.old.id])
          return; // Ignore our own events.

        // If local modification exists, ignore remote deletion.
        store.get(change.old.id)
         .then(function (existing) {
           if (existing.data._status != 'synced')
             return;
           // Delete completely from local DB.
           store.delete(change.old.id, {virtual: false})
             .then(removeMarker.bind(undefined, change.old));
         });
      });
    });
  }
}

window.addEventListener("DOMContentLoaded", main);
