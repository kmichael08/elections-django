/**
 * Get the full name of the unit.
 * @param ancestor
 * @returns {string} full name of the unit.
 */
function unit_name(ancestor) {
    "use strict";
    return ancestor.type + ' ' + ancestor.name;
}
