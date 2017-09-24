from board.models import board
from django.views.generic import ListView
from django.shortcuts import redirect


class boardLV(ListView):

    model = board
    template_name = "seeboard.html"
    context_object_name = "board_list"
    queryset = board.objects.all().values_list('board_description','board_user_username_id')

def BoardCreate(request):

    board.objects.create(board_description=request.POST['board_name'],board_user_username_id=request.user.username)
    return redirect('/board/seeboard')

