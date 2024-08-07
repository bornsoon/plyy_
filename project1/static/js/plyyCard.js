// 플리 카드
function fetchPlyy() {
    fetch('/api/main/plyy')
    .then(response =>  response.json())
    .then(data => {
        document.title = 'PLYY';
        const plyyList = document.getElementById('mainList');
        data.forEach((plyy, index) => {
            let dateTagId = 'dateTag' + index;
            let plyyTagId = 'plyyTag' + index;
            let heartId = 'heart' + index; 
            const plyyCard = document.createElement('li');
            plyyCard.innerHTML = 
                `<a href="./plyy/${plyy.id}">` +
                    '<div class="plyy-card__top">' +
                        `<img src="static/images/${plyy.img}" alt="" class="plyy-card__top__img">` +
                        `<div id="${dateTagId}" class="badge green"></div>` + 
                        '<div class="plyy-card__top__tag-list">' +
                            `<div class="badge tag"># ${plyy.genre}</div>` +
                            `<div id="${plyyTagId}" class="badge tag"></div>` +
                        '</div>' +
                        `<button class="btn-plike--unfill" id=${heartId} aria-label="플레이리스트 좋아요 즐겨찾기"></button>` +
                    '</div>' +
                    '<div class="plyy-card__bottom">' +
                        '<div>' +
                            `<div class="plyy-card__bottom__title fs16"><span class="hide">${plyy.title}</span>${plyy.title}</div>` +
                            '<div class="align both">' +
                                `<div class="plyy-card__bottom--cname fs12"><span class="hide">${plyy.curator}</span>${plyy.curator}</div>` +
                                `<div class="plyy-card__bottom--count fs12"><span class="hide">${plyy.tracks}곡 | ${plyy_time(plyy.times)}</span>${plyy.tracks}곡 | ${plyy_time(plyy.times)}</div>` +
                            '</div>' +
                        '</div>' +
                    '</div>' +
                '</a>';
            plyyList.appendChild(plyyCard);

            // NEW | UPDATE 태그
            let dateTag = document.getElementById(dateTagId);
            isDate = isTag(plyy.generate, plyy.update);
            if (isDate) {
                dateTag.innerHTML = '<span class="hide">' + isDate + '</span>' + isDate;
            } else {
                dateTag.style.visibility = "hidden";
            };
            
            // 플리태그 2개까지
            let plyy_tag = document.getElementById(plyyTagId);
            if (plyy.tag) {
                plyy_tag.textContent = '#' + plyy.tag;
            } else {
                plyy_tag.style.visibility = "hidden";
            };

            // 플리 하트
            let heart = document.getElementById(heartId);
            heart.addEventListener('click', function(event) {
                event.preventDefault();
                // event.stopPropagation();  # 이벤트용 처리 막기
            });
        })
    })
    .catch(error => console.error('데이터를 처리하는 과정에서 오류가 발생하였습니다.'))
};