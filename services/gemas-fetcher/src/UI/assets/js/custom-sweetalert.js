function errorSwal(msg) {
    Swal.fire({
        html:
            `<div class="w-100" style="font-size:14px">
                <div class="header bg-red w-100 p-3 text-white text-start" style="border-radius: 5px 5px 0 0;">
                    <i class="fa fa-info-circle"></i> Alert
                </div>
                <div class="swal2-icon swal2-error swal2-icon-show" style="display: flex;"><span class="swal2-x-mark">
                    <span class="swal2-x-mark-line-left"></span>
                    <span class="swal2-x-mark-line-right"></span>
                </span>
                </div>
                <div class="p-4" style="font-size:16px; font-weight: 700;">
                    <p>${msg}</p>
                </div>
            </div>`,
        showCancelButton: false,
        showConfirmButton: false,
        timer: 2000,
        })
}

function successSwal(msg) {
    Swal.fire({
        html:
            `<div class="w-100" style="font-size:14px">
                <div class="header bg-success w-100 p-3 text-white text-start" style="border-radius: 5px 5px 0 0;">
                    <i class="fa fa-check-circle"></i> Alert
                </div>
                <div class="swal2-icon swal2-success swal2-icon-show" style="display: flex;">
                <div class="swal2-success-circular-line-left" style="background-color: rgb(255, 255, 255);"></div>
                <span class="swal2-success-line-tip"></span> <span class="swal2-success-line-long"></span>
                <div class="swal2-success-ring"></div> <div class="swal2-success-fix" style="background-color: rgb(255, 255, 255);"></div>
                <div class="swal2-success-circular-line-right" style="background-color: rgb(255, 255, 255);"></div>
                </div>
                <div class="p-4" style="font-size:16px; font-weight: 700;">
                    <p>${msg}</p>
                </div>
            </div>`,
        showCancelButton: false,
        showConfirmButton: false,
        timer: 2000,
        })
}