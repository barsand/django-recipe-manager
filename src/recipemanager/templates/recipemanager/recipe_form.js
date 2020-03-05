<script>
function display2required(display_attr) {
    if (display_attr == 'none') return false
    else return true
}

function get_parent(element_id, parent_tag) {
    element = $('#' + element_id);
    parent_el = null
    Array.from(element.parents()).forEach(function (el) {
        if (el.tagName  == parent_tag) {
            parent_el = el;
            return
        }
    });
    return parent_el;
}

function swap_row_visibility(clicked_element, affected_element) {
    var parent_table = null, parent_row= null;
    var clicked_element_parent_table = get_parent(clicked_element.id, 'TABLE');
    var clicked_element_parent_row = get_parent(clicked_element.id, 'TR');
    var affected_element_parent_table = get_parent(affected_element.id, 'TABLE');
    var affected_element_parent_row = get_parent(affected_element.id, 'TR');
    var element_ean = clicked_element.id.split('-');
    element_ean = element_ean[element_ean.length - 1];
    var clicked_attr_value = null;
    var affected_attr_value = null;

    var quantity_field = document.getElementById('quantity-' + element_ean);

    if (clicked_element_parent_table.id == 'recipe-listing') {
        if (!clicked_element.checked) {
            quantity_field.required = false;
            clicked_attr_value = 'none';
            affected_attr_value = 'table-row';
        }
    }
    else if (clicked_element_parent_table.id == 'standby-listing') {
        if (clicked_element.checked) {
            quantity_field.required = true;
            clicked_attr_value = 'none';
            affected_attr_value = 'table-row';
        }
    }
    clicked_element_parent_row.style.display = clicked_attr_value;
    affected_element_parent_row.style.display = affected_attr_value;
}

$(document).ready( function () {
    $('#standby-listing').DataTable();

    $('.checkbox-toggler').click(function() {
        var current_class = null, clicked_element = this;
        this.className.split(' ').forEach(function (c) {
            if (c.slice(0, 4) == 'ean-') {
                current_ean_class = c;
            }
        });

        Array.from(document.getElementsByClassName(current_ean_class)).forEach(function (checkbox) {
            if(checkbox.id != clicked_element.id){
                checkbox.checked = clicked_element.checked;
                swap_row_visibility(clicked_element, checkbox);
            }
        });
    });
} );
</script>
