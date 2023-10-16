const showFilterButton = document.getElementById('filter-button');
const showActionButton = document.querySelectorAll('.action-modal-button');
const applyFilterFromModalButton = document.getElementById('applyFilterFromModalButton');
const applyFilterFromPanelButton = document.getElementById('applyFilterFromPanelButton');
const tableRows = document.querySelectorAll("tbody > tr" );
const selectAllCheckBox = document.getElementById('select-all-checkbox');
const listCheckBoxes = document.querySelectorAll('.list-checkbox');
const actionButtonsWithIds = document.querySelectorAll('.get-ids-param')

if (showFilterButton) {
    showFilterButton.addEventListener('click', showFilter);
    applyFilterFromModalButton.addEventListener('click', applyFilterFromModal);
    applyFilterFromPanelButton.addEventListener('click', applyFilterFromPanel);
}

showActionButton.forEach((element) => {
    element.addEventListener('click', showActions);
})

tableRows.forEach((element) => {
    if (element.hasAttribute('data-detail-url')) {
        element.addEventListener('click', openTableRow);
    }
})

document.addEventListener('DOMContentLoaded', setFilter);

if (selectAllCheckBox) {
    selectAllCheckBox.addEventListener('click', selectAll);
}

listCheckBoxes.forEach(box => {
    box.addEventListener('click', selectOne);
})

actionButtonsWithIds.forEach(button => {
    button.addEventListener('click', callActionWithIds);
})

function openTableRow() {
    // console.log(this)
    window.location = this.getAttribute('data-detail-url');
}

function selectAll() {
    const currentValue = selectAllCheckBox.checked;
    listCheckBoxes.forEach(checkBox => {
        checkBox.checked = currentValue;
    })
}

function selectOne(e) {
    e.stopPropagation();
    selectAllCheckBox.checked = false;
}

function showFilter() {
    let modal = document.getElementById('filter-modal');
    let closeActions = modal.querySelectorAll('.filter-modal-close');
    closeActions.forEach((action) => {
        action.addEventListener('click', hideFilter);
    })
    modal.classList.add('is-active');
}

function showActions() {
    let modal = document.getElementById('action-modal');
    let closeActions = modal.querySelectorAll('.action-modal-close');
    closeActions.forEach((action) => {
        action.addEventListener('click', hideActions);
    })
    modal.classList.add('is-active');
}

function hideActions() {
    let modal = document.getElementById('action-modal');
    modal.classList.remove('is-active');
}


function hideFilter() {
    let modal = document.getElementById('filter-modal');
    modal.classList.remove('is-active');
}

function setFilter() {
    let queryString = window.location.href.split('?')[1];
    if (queryString) {
        let terms = document.querySelectorAll('input, .filter-term');
        let queries = queryString.split('&');

        queries.forEach((query) => {
            terms.forEach((term) => {
                if (term.name === query.split('=')[0]) {
                    term.value = decodeURIComponent(query.split('=')[1]);
                }
            })
        })
    }
}

function applyFilter(terms) {
    const baseURl = window.location.href.split('?')[0];
    let urlQueryString= '?';

    terms.forEach((term) => {
        if (term.value && term.value !== '') {
            urlQueryString += term.name + '=' + encodeURIComponent(term.value) + '&';
        }
    })

    window.location.assign(baseURl + urlQueryString);
}

function applyFilterFromModal() {
    let modal = document.getElementById('filter-modal');
    let terms = modal.querySelectorAll('input, .filter-term');
    applyFilter(terms);
}

function applyFilterFromPanel() {
    let panel = document.getElementById('filter-panel');
    let terms = panel.querySelectorAll('input, .filter-term');
    applyFilter(terms);
}

function resetFilter() {
    window.location.assign(window.location.href.split('?')[0]);
}

function getSelectedIdsUrlParam() {
    let ids = [];
    listCheckBoxes.forEach(box=> {
        if (box.checked) {
            ids.push(box.name);
        }
    })
    if (selectAllCheckBox.checked || !ids.length) {
        return ''
    }
    return 'list__id__in=' + ids
}

function callActionWithIds() {
    this.href += '&' + getSelectedIdsUrlParam();
}