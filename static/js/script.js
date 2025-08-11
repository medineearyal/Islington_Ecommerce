const swiper = new Swiper('.swiper', {
    direction: 'horizontal',
    speed: 500,
    loop: true,
    slidesPerView: 6,

    pagination: {
        el: '.swiper-pagination',
    },

    autoplay: {
        delay: 5000,
        disableOnInteraction: true,
    },

    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
});

const swiperBanner = new Swiper(".swiper-banner", {
    direction: 'horizontal',
    loop: true,
    speed: 500,
    slidesPerView: 1,

    autoplay: {
        delay: 5000,
        disableOnInteraction: true,
    },

    pagination: {
        el: '.swiper-pagination',
        clickable: true,
    },
});

window.addEventListener("DOMContentLoaded", function () {
    const copyrightDate = document.querySelector(".copyright-date");
    if (copyrightDate) {
        copyrightDate.innerHTML = new Date().getFullYear();
    } else {
        copyrightDate.innerHTML = "2025";
    }

    const bestDealRemainingTime = document.getElementById("best-deal-remaining-time");
    if (bestDealRemainingTime) {
        const dealEndTimeIso = bestDealRemainingTime.getAttribute("data-end-date");
        const dealEndTime = new Date(dealEndTimeIso).getTime();

        function updateCountdown(countdownElem, dealEndTime) {
            const now = new Date().getTime();
            let distance = dealEndTime - now;

            if (distance <= 0) {
                countdownElem.innerHTML = "Expired";
                clearInterval(timer);
                return;
            }

            const days = Math.floor(distance / (1000 * 60 * 60 * 24));
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);

            countdownElem.innerHTML = `${days}d : ${hours}h : ${minutes}m : ${seconds}s`;
        }

        updateCountdown(bestDealRemainingTime, dealEndTime);

        const timer = setInterval(() => updateCountdown(bestDealRemainingTime, dealEndTime), 1000);
    }

    const slider = document.getElementById('slider');
    if (slider) {
        const minOutput = document.getElementById('slider-min');
        const maxOutput = document.getElementById('slider-max');

        noUiSlider.create(slider, {
            start: [100, 900],
            connect: true,
            range: {
                'min': 0,
                'max': 1000
            },
            step: 10,
            tooltips: [true, true],
            format: {
                to: value => Math.round(value),
                from: value => Math.round(value)
            }
        });

        slider.noUiSlider.on('update', function (values) {
            minOutput.textContent = values[0];
            maxOutput.textContent = values[1];
        });
    }
});