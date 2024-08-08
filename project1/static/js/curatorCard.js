// 큐레이터 카드
function fetchCurator() {
    fetch('/api/main/curator')
    .then(response => response.json())
    .then(data => {
        document.title = 'PLYY | CURATOR';
        data.forEach((c, index) => {
            let updateTagId = 'updateTag' + index;
            let curatorTagId1 = 'curatorTag1' + index;
            let curatorTagId2 = 'curatorTag2' + index;
            let heartId = 'heart' + index;
            const curatorCard = document.createElement('li');
            curatorCard.innerHTML =
                `<a href="./curator/${c.id}">` +
                    '<div class="curator-card__top">' +
                        `<img src="static/images/${c.img}" alt="" class="curator-card__top__img">` +
                        `<div id="${updateTagId}" class="badge green"><span class="hide">UPDATE</span>UPDATE</div>` +
                        '<div class="curator-card__top__tag-list">' +
                            `<div id="${curatorTagId1}" class="badge tag"></div>` +
                            `<div id="${curatorTagId2}" class="badge tag"></div>` +
                        '</div>' +
                        `<button class="btn-clike--unfill" id=${heartId} aria-label="큐레이터 좋아요 즐겨찾기"></button>` +
                    '</div>' +
                    '<div class="curator-card__bottom">' +
                        '<div>' +
                            `<div class="curator-card__bottom__title fs16"><span class="hide">${c.name}</span>${c.name}</div>` +
                            '<div class="align both">' +
                                `<div class="curator-card__bottom__intro fs12"><span class="hide">${c.intro}</span>${c.intro}</div>` +
                            '</div>' +
                        '</div>' +
                    '</div>' +
                '</a>';
            mainList.appendChild(curatorCard); 
            
            // UPDATE 태그
            let updateTag = document.getElementById(updateTagId);
            let isUpdate = isTag(c.generate, c.update);
            if (!(isUpdate)) {
                updateTag.style.visibility = "hidden";
            };
            
            // 큐레이터의 플리 태그 2개까지
            let curatorTag1 = document.getElementById(curatorTagId1);
            let curatorTag2 = document.getElementById(curatorTagId2);
            let tag = [curatorTag1, curatorTag2];
            if (c.tag == '') {
                tag[0].style.visibility = "hidden";
                tag[1].style.visibility = "hidden";
            }
            c.tag.forEach((element, index) => {
                if (element == '') {
                    tag[index].style.visibility = "hidden";
                } else {
                    tag[index].textContent = '#' + element;
                }
            });

            let heart = document.getElementById(heartId);
            heart.addEventListener('click', function(event) {
                event.preventDefault();
                // event.stopPropagation();  # 이벤트 용 처리 막기
            });
        })
    })
    .catch(error => console.error('데이터를 처리하는 과정에서 오류가 발생하였습니다.'))
};