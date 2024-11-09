document.addEventListener("DOMContentLoaded", function() {
    // Override the _updateOpacity function
    L.TileLayer.prototype._updateOpacity = function() {
        L.DomUtil.setOpacity(this._container, this.options.opacity);
        for (var key in this._tiles) {
            var tile = this._tiles[key];
            L.DomUtil.setOpacity(tile.el, 1); // Set opacity to 1
        }
    };
});