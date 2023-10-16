const queryBlock = document.getElementById('query-block');
const queryInput = document.getElementById('query-input');
const queryInputControl = document.getElementById('query-input-control');
const queryInputSelect = document.getElementById('query-input-select');
const queryInputSelectControl = document.getElementById('query-input-select-control');
const queryInputApply = document.getElementById('query-input-apply');
const queryParamsDropdown = document.getElementById('query-params-dropdown');
const queryParamElements = document.querySelectorAll('.query-param');
const queryParamsElements = document.querySelectorAll('.query-params');
const applyButton = document.getElementById('apply-filter-button');
const resetButton = document.getElementById('reset-filter-button');
const queryTags = document.getElementById('query-tags');
const modalFilterButton = document.getElementById('modal-filter-button');
const filterPanel = document.getElementById('filter-panel');
const filterModal = document.getElementById('filter-modal');
const modalContent = document.getElementById('modal-content');
let activeInput = queryInput;
let query = new URLSearchParams();

applyButton.addEventListener('click', apply);
resetButton.addEventListener('click', reset);
queryInput.addEventListener('focus', showQueryParams);
queryInput.addEventListener('keyup', navigateQueryInput);
queryInputApply.addEventListener('click', applyQueryInput);
queryParamElements.forEach((element) => {
    element.addEventListener('keyup', navigateQueryParams);
})
queryParamElements.forEach((element) => {
    element.addEventListener('mouseup', clickQueryParams);
})
window.onclick = function(event) {
    const dontHide = [
        '#query-block', '#query-input', '#query-params-dropdown', '#param-input',
        '.query-param', '.query-params', '.query-param > p', '#query-operation',
        '#query-operation > span', '#query-operation-select',
        '#query-operation-select > option', '#query-params-dropdown > p > label',
        '#query-params-dropdown > p', '#query-params-dropdown > p > label > input',
        '#query-input-select', '#query-input-select > option'
    ];
    if (!event.target.matches(dontHide)) {
        queryParamsElements.forEach((element) => {
            element.classList.add('is-hidden');
        })
        queryParamsDropdown.classList.add('is-hidden');
  }
}

modalFilterButton.onclick = function (event) {
    modalContent.appendChild(filterPanel);
    filterModal.classList.add('is-active');
}

buildActiveQuery();

function buildActiveQuery() {
    const url = new URL(window.location.href);
    const query = url.searchParams.get('q');
    if (!query) {
        return
    }
    for(let block of JSON.parse(query)) {
        const tagBlock = buildTagBlock();
        for (let param of block) {
            if (Object.prototype.toString.apply(param) === '[object Object]') {
                const tag = buildActiveQueryTag(param);
                tagBlock.appendChild(tag);
            }
            if (Object.prototype.toString.apply(param) === '[object Array]') {
                const tagGroup = buildTagGroup();
                for (let orParam of param) {
                    const tag = buildActiveQueryTag(orParam);
                    tagGroup.appendChild(tag);
                    tagBlock.appendChild(tagGroup);
                }
            }
        }
        if (queryTags.childElementCount > 0) {
            const blockLabel = buildTagBlockLabel();
            queryTags.appendChild(blockLabel);
        }
        queryTags.appendChild(tagBlock)
    }
}

function buildActiveQueryTag(param) {
    let tag = null;
    let displayValue = '';
    let value = null;
    for (let p in param) {
        if (typeof param[p] == 'boolean') {
            value = param[p]
        }
        const element = getParamElement(p, value);
        const dataType = element.getAttribute('data-type');
        const text = getCompleteQueryText(element);
        if (dataType === 'bool') {
            displayValue = element.firstElementChild.text;
        }
        else if (dataType === 'selection') {
            const option = element.querySelector(
                `.param-options option[value="${param[p]}"]`
            );
            displayValue = option.textContent;
        }
        else {
            displayValue = param[p];
        }
        tag = buildTag(text, p, param[p], displayValue);
    }
    return tag
}

function apply() {
    const baseURl = window.location.href.split('?')[0];
    let completeQuery = [];
    const tagBlocks = document.querySelectorAll('.query-tag-block');
    tagBlocks.forEach((tagBlock) => {
        let query = [];
        for (let tag of tagBlock.children) {
            if (tag.classList.contains('query-tag')) {
                const param = tag.getAttribute('data-param');
                let value = tag.getAttribute('data-value');
                if (tag.getAttribute('data-is-bool') === 'true') {
                    value = value === 'true'
                }
                query.push({[param]: value})
            }
            else if (tag.classList.contains('query-tag-group')) {
                let orQuery = [];
                for (let subTag of tag.children) {
                    if (subTag.classList.contains('query-tag')) {
                        const param = subTag.getAttribute('data-param');
                        let value = subTag.getAttribute('data-value');
                        if (subTag.getAttribute('data-is-bool') === 'true') {
                            value = value === 'true'
                        }
                        orQuery.push({[param]: value});
                    }
                }
                if (orQuery.length) {
                    query.push(orQuery);
                }
            }
        }
        completeQuery.push(query);
    })
    window.location.assign(baseURl.concat('?') + 'q='.concat(JSON.stringify(completeQuery)));
}

function reset() {
    const baseURl = window.location.href.split('?')[0];
    window.location.assign(baseURl);
}

function applyQueryInput(event) {
    event.stopPropagation();
    const text = queryInput.getAttribute('data-text');
    const param = queryInput.getAttribute('data-param');
    const value = activeInput.value;
    let displayValue = value
    if (activeInput === queryInputSelect) {
        displayValue = activeInput.selectedOptions[0].textContent
    }
    if (value && param) {
        addQueryTag(text, param, value, displayValue);
    }
    resetQueryInput();
}

function showQueryParams() {
    document.getElementById('query-params-dropdown').classList.remove(
        'is-hidden'
    );
}

function navigateQueryInput(event) {
    if (event.key === 'Enter') {
        applyQueryInput(event);
    }
    if (event.key === 'Escape') {
        queryParamsDropdown.classList.add('is-hidden');
    }
    if (event.key === 'ArrowDown') {
        if (queryParamsDropdown.classList.contains('is-hidden')) {
            queryParamsDropdown.classList.remove('is-hidden');
        }
        if (!queryInput.type in ['date', 'datetime-local', 'number']) {
            queryParamsDropdown.firstElementChild.focus({ focusVisible: true });
        }

    }
}

function clickQueryParams(event) {
    event.stopPropagation();
    const queryParam = event.target.parentElement;
    const queryParams = queryParam.querySelector(
        '.query-params'
    );
    if (queryParams && queryParams.classList.contains('is-hidden')) {
        queryParams.classList.remove('is-hidden');
    }
    else {
        const subQueryParams = queryParam.querySelectorAll(
            '.query-params'
        );
        subQueryParams.forEach((element) => {
            element.classList.add('is-hidden');
        })
    }
    if (!queryParam.querySelector('.query-params')) {
        const completeParam = getCompleteQueryParam(queryParam);
        const dataType = queryParam.getAttribute('data-type');
        const text = getCompleteQueryText(queryParam);
        resetQueryInput();
        setInputType(dataType, completeParam, text,
            queryParam.getAttribute('data-step') || null
        );
        queryInput.select();
        if (dataType === 'bool') {
            let value = queryParam.getAttribute('data-value');
            value = value === 'True';
            addQueryTag(text, completeParam, value, queryParam.firstElementChild.text);
            setInputType('text', '', '');
        }
        else if (dataType === 'selection') {
            const options = queryParam.querySelector('.param-options');
            activeInput = queryInputSelect;
            queryInputSelect.innerHTML = options.innerHTML;
            queryInputSelectControl.classList.remove('is-hidden');
            queryInputControl.classList.add('is-hidden');
            queryInput.setAttribute('data-param', completeParam);
            queryInput.setAttribute('data-text', text);
            document.getElementById('query-text').innerText = text;
        }
    }
}

function navigateQueryParams(event) {
    event.stopPropagation();
    let elementToFocus = null;
    const isSubQuery = event.target.parentElement.classList.contains(
        'query-params'
    );
    const hasSubQuery= event.target.querySelectorAll('.query-params');

    if (event.key === 'ArrowUp') {
        if (event.target.previousElementSibling) {
            elementToFocus = event.target.previousElementSibling;
        }
        else if (event.target.parentElement.id === 'query-params-dropdown') {
            elementToFocus = queryInput;
            elementToFocus.select();
        }
        else if (event.target.parentElement.classList.contains('query-param')) {}
    }
    else if (event.key === 'ArrowDown') {
        elementToFocus = event.target.nextElementSibling;
    }
    else if (event.key === 'Escape') {
        elementToFocus = queryInput;
        elementToFocus.select();
        queryParamsElements.forEach((element) => {
            element.classList.add('is-hidden');
        })

    }
    else if (event.key === 'ArrowRight') {
        if (hasSubQuery) {
            const queryParams= event.target.querySelector('.query-params');
            if (queryParams) {
                queryParams.classList.remove('is-hidden');
                elementToFocus = queryParams.firstElementChild;
            }
        }
    }
    else if (event.key === 'ArrowLeft') {
        if (isSubQuery) {
            elementToFocus = event.target.parentElement.parentElement;
            event.target.parentElement.classList.add('is-hidden');
        }
    }
    if (elementToFocus) {
        elementToFocus.focus();
    }

    if (event.key === 'Enter') {
        const param = event.target.getAttribute('data-param');
        const value = queryInput.value;
        const text = getCompleteQueryText(event.target)
        addQueryTag(text, param, value);
    }
}

function getParamElement(param, value=null) {
    const invert = param.startsWith('~');
    if (invert) {
        param = param.slice(1);
    }
    const parts = param.split('__');
    let selector = '#query-params-dropdown'
    for (let i = 0; i < parts.length; i++) {
        selector += ` div[data-param="${parts[i]}"]`
    }
    if (invert) {
        selector = selector.trimEnd();
        selector += `[data-param-invert="true"]`;
    }
    if (typeof value == 'boolean') {
        if (value) {
            selector += `[data-value="True"]`;
        } else {
            selector += `[data-value="False"]`;
        }
    } else if (value) {
        selector += `[data-value="${value}"]`;
    }
    return document.querySelector(selector)
}

function getQueryTextParts(element) {
    let currentElement = element;
    let names = [];
    names.push(currentElement.firstElementChild.innerText);
    while (currentElement.parentElement.parentElement.classList.contains('query-param')) {
        currentElement = currentElement.parentElement.parentElement;
        names.push(currentElement.firstElementChild.innerText);
    }
    return names.reverse()
}

function getCompleteQueryText(element) {
    let names = getQueryTextParts(element);
    return names.join(' \u2192 ')
}

function getCompleteQueryParam(element) {
    let currentElement = element;
    const invert = currentElement.getAttribute('data-param-invert');
    let params = [];
    params.push(currentElement.getAttribute('data-param'));
    while (currentElement.parentElement.parentElement.classList.contains('query-param')) {
        currentElement = currentElement.parentElement.parentElement;
        params.push(currentElement.getAttribute('data-param'))
    }
    let paramString = params.reverse().join('__')

    if (invert === 'true') {
        paramString = '~'.concat(paramString)
    }
    return paramString
}

function addQueryTag(text, param, value, displayValue) {
    const operation = document.getElementById('query-operation-select').value;
    const selectedTag= queryTags.querySelector('.selected-query-tag');
    if (!queryTags.childElementCount) {
        let tagBlock = buildTagBlock();
        let tag = buildTag(text, param,  value, displayValue);
        tagBlock.appendChild(tag);
        queryTags.appendChild(tagBlock);
    }
    else if (operation === 'and' && selectedTag) {
        selectedTag.parentElement.appendChild(buildTag(text, param, value, displayValue));
    }
    else if (operation === 'and' && !selectedTag) {
        queryTags.lastElementChild.appendChild(buildTag(text, param, value, displayValue));
    }
    else if (operation === 'or' && selectedTag) {
        if (selectedTag.classList.contains('query-tag-group')) {
            let tag = buildTag(text, param, value, displayValue);
            selectedTag.appendChild(tag);
        }
        else {
            let tagGroup = buildTagGroup();
            let tag = buildTag(text, param, value, displayValue);
            selectedTag.parentElement.insertBefore(tagGroup, selectedTag);
            tagGroup.appendChild(selectedTag);
            tagGroup.appendChild(tag);
            selectedTag.classList.remove('selected-query-tag');
            tagGroup.classList.add('selected-query-tag');
        }
    }
    else if (operation === 'or' && !selectedTag) {
        const tagBlock = buildTagBlock();
        const tag = buildTag(text, param, value, displayValue)
        const tagBlockLabel = buildTagBlockLabel();
        tagBlock.appendChild(tag);
        queryTags.appendChild(tagBlockLabel);
        queryTags.appendChild(tagBlock);
    }
    apply();
}

function unselectSingleObject(pk) {
    const tag = buildActiveQueryTag(JSON.parse(`{"~id__exact": ${pk}}`));
    if (!queryTags.childElementCount) {
        const tagBlock = buildTagBlock();
        tagBlock.appendChild(tag);
        queryTags.appendChild(tagBlock);
    } else {
        queryTags.lastElementChild.appendChild(tag);
    }
    apply();
}

function buildTagBlock() {
    let container = document.createElement('div');
    container.classList.add('query-tag-block');
    return container
}

function buildTagBlockLabel() {
    const blockLabel = document.createElement('span');
    blockLabel.innerText = queryTags.getAttribute('data-or-label');
    blockLabel.classList.add('query-or-label');
    return blockLabel
}

function buildTagGroup() {
    let container= document.createElement('div');
    container.classList.add('query-tag-group');
    container.addEventListener('click', setSelectedTag);
    return container
}

function buildTag(text, param, value, displayValue) {
    let container = document.createElement('div');
    let textSpan = document.createElement('span');
    let deleteSpan = document.createElement('span');
    let deleteButton = document.createElement('button');
    container.classList.add('query-tag');
    container.tabIndex = -1;
    textSpan.classList.add('query-tag-text', 'is-size-6', 'is-unselectable');
    if (displayValue) {
        text = text.concat(': ', displayValue);
    }
    textSpan.innerText = text;
    deleteSpan.classList.add(
        'is-flex', 'is-flex-direction-column',
        'is-justify-content-space-around', 'ml-1'
    );
    deleteButton.classList.add('delete');
    deleteSpan.appendChild(deleteButton);
    container.appendChild(textSpan);
    container.appendChild(deleteSpan);
    container.addEventListener('click', setSelectedTag);
    deleteButton.addEventListener('click', deleteTag);
    container.setAttribute('data-param', param);
    container.setAttribute('data-value', value);
    container.setAttribute('data-is-bool', String(typeof value === 'boolean'));
    return container
}

function setSelectedTag(event) {
    event.stopPropagation();
    let target = event.currentTarget
    if (target.parentElement.classList.contains('query-tag-group')) {
        target = event.currentTarget.parentElement;
    }
    const toDeactivate = target.classList.contains('selected-query-tag');
    const selectedTags= queryBlock.querySelectorAll('.selected-query-tag');
    selectedTags.forEach((element) => {
        element.classList.remove('selected-query-tag');
    })
    if (!toDeactivate) {
        target.classList.add('selected-query-tag');
    }
}

function deleteTag(event) {
    event.stopPropagation();
    const tag = event.target.closest('.query-tag');
    let tagGroup = tag.parentElement;
    tagGroup.removeChild(tag);
    while (tagGroup.classList.contains('query-tag-group')) {
        if (!tagGroup.childElementCount) {
            let parent = tagGroup.parentElement;
            parent.removeChild(tagGroup);
            tagGroup = parent;
        }
        else if (tagGroup.childElementCount === 1) {
            let parent = tagGroup.parentElement
            let child = tagGroup.firstElementChild
            if (tagGroup.classList.contains('selected-query-tag')) {
                child.classList.add('selected-query-tag');
            }
            parent.appendChild(child);
            parent.removeChild(tagGroup);
            tagGroup = parent.parentElement;
        }
        else {
            break
        }

    }
    if (tagGroup.classList.contains('query-tag-block') && !tagGroup.childElementCount) {
        const previousSibling = tagGroup.previousElementSibling;
        const nextSibling = tagGroup.nextElementSibling;
        if (previousSibling && previousSibling.classList.contains('query-or-label')) {
            tagGroup.parentElement.removeChild(previousSibling);
        }
        if (nextSibling && nextSibling.classList.contains('query-or-label')) {
            nextSibling.remove();
        }
        tagGroup.parentElement.removeChild(tagGroup);
    }
    apply();
}

function setInputType(inputType, param, text, step=null) {
    queryInput.setAttribute('type', inputType);
    queryInput.setAttribute('data-param', param);
    queryInput.setAttribute('data-text', text);
    document.getElementById('query-text').innerText = text;
    if (step) {
        queryInput.step = step
    }
}

function resetQueryInput() {
    queryInput.setAttribute('type', 'text');
    queryInputSelectControl.classList.add('is-hidden');
    queryInputControl.classList.remove('is-hidden');
    activeInput = queryInput;
    queryInput.select();
}
