from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Q
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db import transaction
import openpyxl
from ...models import Phi, ChiTietPhiTheoThang, HoKhau
from ...forms.khoanthu_form import PhiForm, CapNhatPhiSinhHoatForm, CapNhatPhiSinhHoat, CapNhatPhiForm, UploadPhiSinhHoatForm
import logging

logger = logging.getLogger(__name__)


def quanly_khoanthu(request):
    query = request.GET.get('q', '').strip()
    month_fees = Phi.objects.select_related('ho_khau').all()

    if query:
        month_fees = month_fees.filter(
            Q(ho_khau__so_can_ho__icontains=query) |
            Q(ho_khau__toa_nha__icontains=query) |
            Q(ho_khau__chu_ho__ho_ten__icontains=query)
        )

    months = list(range(1, 13))
    fee_totals = {}

    for phi in month_fees:
        ho_khau = phi.ho_khau
        ho_khau_id = ho_khau.id
        so_can_ho = ho_khau.so_can_ho

        if ho_khau_id not in fee_totals:
            fee_totals[ho_khau_id] = {
                'so_can_ho': so_can_ho,
                'monthly_fees': [0] * 12,  
                'payment_status': {}  
            }

        for month in months:
            so_tien = ChiTietPhiTheoThang.objects.filter(
                phi=phi,
                thang=month
            ).aggregate(total=Sum('so_tien'))['total'] or 0

            fee_totals[ho_khau_id]['monthly_fees'][month - 1] += so_tien

            chi_tiet_phi = ChiTietPhiTheoThang.objects.filter(
                phi=phi,
                thang=month
            ).first()

            if chi_tiet_phi:
                fee_totals[ho_khau_id]['payment_status'][month] = chi_tiet_phi.da_dong

    return render(request, 'ketoan/khoanthu/quanly_khoanthu.html', {
        'fee_totals': fee_totals,
        'query': query,
        'months': months,
    })

def chi_tiet_phi(request, ho_khau_id):
    ho_khau = get_object_or_404(HoKhau, id=ho_khau_id)
    months = list(range(1, 13))
    loai_phi_list = ['Dịch vụ', 'Quản lý', 'Sinh hoạt', 'Gửi xe']
    chi_tiet_phi = {loai: [] for loai in loai_phi_list}

    for month in months:
        for loai in loai_phi_list:
            tong = ChiTietPhiTheoThang.objects.filter(
                phi__ho_khau=ho_khau,
                phi__loai_phi=loai,
                thang=month
            ).aggregate(total=Sum('so_tien'))['total'] or 0
            chi_tiet_phi[loai].append(tong)

    return render(request, 'ketoan/khoanthu/chi_tiet_phi.html', {
        'ho_khau': ho_khau,
        'months': months,
        'chi_tiet_phi': chi_tiet_phi,
    })

def thong_ke_khoan_phi(request):
    loai_phi = request.GET.get('loai_phi', '')
    thang = int(request.GET.get('thang', 1))
    nam = int(request.GET.get('nam', timezone.now().year))

    if loai_phi:
        phi_records = Phi.objects.filter(loai_phi=loai_phi, nam=nam)
    else:
        phi_records = Phi.objects.filter(nam=nam)

    thong_ke = []
    for phi in phi_records:
        chi_tiet = ChiTietPhiTheoThang.objects.filter(phi=phi, thang=thang).first()
        if chi_tiet:
            thong_ke.append({
                'ho_khau': phi.ho_khau,
                'loai_phi': phi.loai_phi,
                'so_tien': chi_tiet.so_tien,
            })

    return render(request, 'ketoan/khoanthu/thong_ke_khoan_phi.html', {
        'thong_ke': thong_ke,
        'loai_phi': loai_phi,
        'thang': thang,
        'nam': nam,
    })

@require_POST
def xac_nhan_thanh_toan(request, ho_khau_id):
    thang = request.POST.get('thang')
    if not thang:
        messages.error(request, "Vui lòng chọn tháng để thanh toán.")
        return redirect('chi_tiet_phi', ho_khau_id=ho_khau_id)

    chi_tiet_phi = ChiTietPhiTheoThang.objects.filter(
        phi__ho_khau_id=ho_khau_id,
        thang=thang,
        da_dong=False  
    )

    if chi_tiet_phi.exists():
        # Cập nhật trạng thái thanh toán cho tất cả các bản ghi chưa thanh toán
        for phi in chi_tiet_phi:
            phi.da_dong = True
            phi.save()  

        # Cập nhật lại phí trong `quanly_khoanthu` cho tất cả loại phí
        for phi in chi_tiet_phi:
            phi.phi.cap_nhat_phi()  

        messages.success(request, f"Thanh toán cho tháng {thang} đã được xác nhận và phí đã được đặt về 0!")
    else:
        messages.error(request, "Không tìm thấy các khoản phí chưa thanh toán cho tháng này.")

    return redirect('quanly_khoanthu')  # Quay lại trang quản lý khoản thu

def cap_nhat_phi_sinh_hoat(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        wb = openpyxl.load_workbook(excel_file)
        sheet = wb.active

        for row in sheet.iter_rows(min_row=2, values_only=True):  
            so_can_ho = row[0]
            tien_dien = row[1] if row[1] is not None else 0
            tien_nuoc = row[2] if row[2] is not None else 0
            tien_internet = row[3] if row[3] is not None else 0

            # Tìm đối tượng HoKhau dựa trên so_can_ho
            try:
                ho_khau = HoKhau.objects.get(so_can_ho=so_can_ho)
            except HoKhau.DoesNotExist:
                messages.error(request, f"Hộ khẩu với số căn hộ {so_can_ho} không tồn tại.")
                continue  

            thang = int(request.POST.get('thang')) 
            nam = timezone.now().year

            cap_nhat_phi_sinh_hoat, created = CapNhatPhiSinhHoat.objects.update_or_create(
                ho_khau=ho_khau,
                thang=thang,
                nam=nam,
                defaults={
                    'tien_dien': tien_dien,
                    'tien_nuoc': tien_nuoc,
                    'tien_internet': tien_internet,
                }
            )

            if created:
                messages.success(request, f"Cập nhật phí sinh hoạt cho hộ khẩu {so_can_ho} thành công.")
            else:
                messages.success(request, f"Cập nhật phí sinh hoạt cho hộ khẩu {so_can_ho} thành công (đã cập nhật).")

        return redirect('quanly_khoanthu')

    else:
        form = UploadPhiSinhHoatForm()

    return render(request, 'ketoan/khoanthu/cap_nhat_phi_sinh_hoat.html', {'form': form})

def thong_ke_phi_quan_ly(request):

    query = request.GET.get('q', '').strip()

    phi_records = Phi.objects.filter(loai_phi='Quản lý').select_related('ho_khau')

    if query:
        phi_records = phi_records.filter(ho_khau__so_can_ho__icontains=query)

    months = list(range(1, 13))
    fee_totals = {}

    for phi in phi_records:
        ho_khau = phi.ho_khau
        ho_khau_id = ho_khau.id
        so_can_ho = ho_khau.so_can_ho

        if ho_khau_id not in fee_totals:
            fee_totals[ho_khau_id] = {
                'so_can_ho': so_can_ho,
                'monthly_fees': [0] * 12,  
                'payment_status': {} 
            }

        for month in months:
            so_tien = ChiTietPhiTheoThang.objects.filter(
                phi=phi,
                thang=month
            ).aggregate(total=Sum('so_tien'))['total'] or 0

            fee_totals[ho_khau_id]['monthly_fees'][month - 1] += so_tien

            chi_tiet_phi = ChiTietPhiTheoThang.objects.filter(
                phi=phi,
                thang=month
            ).first()

            if chi_tiet_phi:
                fee_totals[ho_khau_id]['payment_status'][month] = chi_tiet_phi.da_dong

    return render(request, 'ketoan/khoanthu/thong_ke_phi_quan_ly.html', {
        'fee_totals': fee_totals,
        'query': query,
        'months': months,
    })

def thong_ke_phi_dich_vu(request):
    query = request.GET.get('q', '').strip()

    phi_records = Phi.objects.filter(loai_phi='Dịch vụ').select_related('ho_khau')

    if query:
        phi_records = phi_records.filter(ho_khau__so_can_ho__icontains=query)

    months = list(range(1, 13))
    fee_totals = {}

    for phi in phi_records:
        ho_khau = phi.ho_khau
        ho_khau_id = ho_khau.id
        so_can_ho = ho_khau.so_can_ho

        if ho_khau_id not in fee_totals:
            fee_totals[ho_khau_id] = {
                'so_can_ho': so_can_ho,
                'monthly_fees': [0] * 12,  
                'payment_status': {} 
            }

        for month in months:
            so_tien = ChiTietPhiTheoThang.objects.filter(
                phi=phi,
                thang=month
            ).aggregate(total=Sum('so_tien'))['total'] or 0

            fee_totals[ho_khau_id]['monthly_fees'][month - 1] += so_tien

            chi_tiet_phi = ChiTietPhiTheoThang.objects.filter(
                phi=phi,
                thang=month
            ).first()

            if chi_tiet_phi:
                fee_totals[ho_khau_id]['payment_status'][month] = chi_tiet_phi.da_dong

    return render(request, 'ketoan/khoanthu/thong_ke_phi_dich_vu.html', {
        'fee_totals': fee_totals,
        'query': query,
        'months': months,
    })

def thong_ke_phi_gui_xe(request):
    query = request.GET.get('q', '').strip()

    phi_records = Phi.objects.filter(loai_phi='Gửi xe').select_related('ho_khau')

    if query:
        phi_records = phi_records.filter(ho_khau__so_can_ho__icontains=query)

    months = list(range(1, 13))
    fee_totals = {}

    for phi in phi_records:
        ho_khau = phi.ho_khau
        ho_khau_id = ho_khau.id
        so_can_ho = ho_khau.so_can_ho

        if ho_khau_id not in fee_totals:
            fee_totals[ho_khau_id] = {
                'so_can_ho': so_can_ho,
                'monthly_fees': [0] * 12,  
                'payment_status': {} 
            }

        for month in months:
            so_tien = ChiTietPhiTheoThang.objects.filter(
                phi=phi,
                thang=month
            ).aggregate(total=Sum('so_tien'))['total'] or 0

            fee_totals[ho_khau_id]['monthly_fees'][month - 1] += so_tien

            chi_tiet_phi = ChiTietPhiTheoThang.objects.filter(
                phi=phi,
                thang=month
            ).first()

            if chi_tiet_phi:
                fee_totals[ho_khau_id]['payment_status'][month] = chi_tiet_phi.da_dong

    return render(request, 'ketoan/khoanthu/thong_ke_phi_gui_xe.html', {
        'fee_totals': fee_totals,
        'query': query,
        'months': months,
    })

def thong_ke_phi_sinh_hoat(request):
    query = request.GET.get('q', '').strip()

    phi_records = Phi.objects.filter(loai_phi='Sinh hoạt').select_related('ho_khau')

    if query:
        phi_records = phi_records.filter(ho_khau__so_can_ho__icontains=query)

    months = list(range(1, 13))
    fee_totals = {}

    for phi in phi_records:
        ho_khau = phi.ho_khau
        ho_khau_id = ho_khau.id
        so_can_ho = ho_khau.so_can_ho

        if ho_khau_id not in fee_totals:
            fee_totals[ho_khau_id] = {
                'so_can_ho': so_can_ho,
                'monthly_fees': [0] * 12, 
                'payment_status': {} 
            }

        for month in months:
            so_tien = ChiTietPhiTheoThang.objects.filter(
                phi=phi,
                thang=month
            ).aggregate(total=Sum('so_tien'))['total'] or 0

            fee_totals[ho_khau_id]['monthly_fees'][month - 1] += so_tien

            chi_tiet_phi = ChiTietPhiTheoThang.objects.filter(
                phi=phi,
                thang=month
            ).first()

            if chi_tiet_phi:
                fee_totals[ho_khau_id]['payment_status'][month] = chi_tiet_phi.da_dong

    return render(request, 'ketoan/khoanthu/thong_ke_phi_sinh_hoat.html', {
        'fee_totals': fee_totals,
        'query': query,
        'months': months,
    })

def chi_tiet_phi_sinh_hoat(request, ho_khau_id):
    ho_khau = get_object_or_404(HoKhau, id=ho_khau_id)
    
    phi_sinh_hoat_details = CapNhatPhiSinhHoat.objects.filter(ho_khau=ho_khau).order_by('thang')

    return render(request, 'ketoan/khoanthu/chi_tiet_phi_sinh_hoat.html', {
        'ho_khau': ho_khau,
        'phi_sinh_hoat_details': phi_sinh_hoat_details,
    })

