from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from ...models import DanhSachPhiDongGop, DongGopPhi, HoKhau, NhanKhau
from ...forms.donggopphi_form import DanhSachPhiDongGopForm, DongGopPhiForm
from django.db.models import Sum

def thong_ke_dong_gop(request):
    # Lấy từ GET parameter nếu có
    query = request.GET.get('q', '').strip()

    # Lọc các khoản đóng góp theo tên hoặc thông tin cần tìm kiếm
    dong_gop_records = DanhSachPhiDongGop.objects.all()

    if query:
        dong_gop_records = dong_gop_records.filter(ten_phi__icontains=query)

    return render(request, 'ketoan/donggop/thong_ke_dong_gop.html', {
        'dong_gop_records': dong_gop_records,
        'query': query
    })

def chi_tiet_dong_gop(request, ten_phi):
    # Lấy khoản đóng góp theo tên
    dong_gop = get_object_or_404(DanhSachPhiDongGop, ten_phi=ten_phi)

    # Lấy tất cả các hộ gia đình đã đóng góp vào khoản đóng góp này
    dong_gop_details = DongGopPhi.objects.filter(phi=dong_gop)

    # Thêm mới khoản đóng góp
    if request.method == 'POST':
        form = DongGopPhiForm(request.POST)
        if form.is_valid():
            # Lưu khoản đóng góp
            new_dong_gop = form.save(commit=False)
            new_dong_gop.phi = dong_gop  # Gắn phi vào khoản đóng góp
            new_dong_gop.save()
            messages.success(request, f"Thêm đóng góp mới cho khoản {dong_gop.ten_phi} thành công.")
            return redirect('chi_tiet_dong_gop', ten_phi=dong_gop.ten_phi)

    else:
        form = DongGopPhiForm()

    return render(request, 'ketoan/donggop/chi_tiet_dong_gop.html', {
        'dong_gop': dong_gop,
        'dong_gop_details': dong_gop_details,
        'form': form
    })

# Thêm khoản đóng góp
def them_dong_gop(request):
    if request.method == 'POST':
        form = DanhSachPhiDongGopForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thêm khoản đóng góp thành công!")
            return redirect('thong_ke_dong_gop')
    else:
        form = DanhSachPhiDongGopForm()

    return render(request, 'ketoan/donggop/them_dong_gop.html', {'form': form})

# Sửa khoản đóng góp
def sua_dong_gop(request, id):
    dong_gop = get_object_or_404(DanhSachPhiDongGop, ten_phi=id)  # Tìm kiếm bằng 'ten_phi'

    if request.method == 'POST':
        form = DanhSachPhiDongGopForm(request.POST, instance=dong_gop)
        if form.is_valid():
            form.save()
            messages.success(request, "Cập nhật khoản đóng góp thành công!")
            return redirect('thong_ke_dong_gop')  # Trở về trang thống kê
    else:
        form = DanhSachPhiDongGopForm(instance=dong_gop)

    return render(request, 'ketoan/donggop/sua_dong_gop.html', {'form': form})

# Xóa khoản đóng góp
def xoa_dong_gop(request, id):
    dong_gop = get_object_or_404(DanhSachPhiDongGop, ten_phi=id)  # Tìm kiếm bằng 'ten_phi'

    if request.method == 'POST':
        dong_gop.delete()
        messages.success(request, "Xóa khoản đóng góp thành công!")
        return redirect('thong_ke_dong_gop')  # Trở về trang thống kê

    return render(request, 'ketoan/donggop/xoa_dong_gop.html', {'dong_gop': dong_gop})

def sua_dong_gop_ho(request, id):
    dong_gop = get_object_or_404(DongGopPhi, id=id)

    if request.method == 'POST':
        form = DongGopPhiForm(request.POST, instance=dong_gop)
        if form.is_valid():
            form.save()
            messages.success(request, "Cập nhật đóng góp thành công!")
            return redirect('chi_tiet_dong_gop', ten_phi=dong_gop.phi.ten_phi)
    else:
        form = DongGopPhiForm(instance=dong_gop)

    return render(request, 'ketoan/donggop/sua_dong_gop_ho.html', {'form': form})

def xoa_dong_gop_ho(request, id):
    dong_gop = get_object_or_404(DongGopPhi, id=id)

    if request.method == 'POST':
        dong_gop.delete()
        messages.success(request, "Đã xóa đóng góp của hộ gia đình!")
        return redirect('chi_tiet_dong_gop', ten_phi=dong_gop.phi.ten_phi)

    return render(request, 'ketoan/donggop/xoa_dong_gop_ho.html', {'dong_gop': dong_gop})

def them_dong_gop_ho(request, ten_phi):
    phi = get_object_or_404(DanhSachPhiDongGop, ten_phi=ten_phi)

    if request.method == 'POST':
        form = DongGopPhiForm(request.POST)
        if form.is_valid():
            # Gán phi đã được chọn vào form
            dong_gop_ho = form.save(commit=False)
            dong_gop_ho.phi = phi
            dong_gop_ho.save()
            messages.success(request, "Đóng góp của hộ gia đình đã được thêm thành công!")
            return redirect('chi_tiet_dong_gop', ten_phi=phi.ten_phi)
    else:
        form = DongGopPhiForm()

    return render(request, 'ketoan/donggop/them_dong_gop_ho.html', {'form': form, 'phi': phi})
