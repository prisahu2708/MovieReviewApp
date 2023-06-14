from rest_framework import permissions

class IsAdminOrReadOnly(permissions.IsAdminUser):
     
    def has_permission(self,request,view):
        #admin_permission = super().has_permission(self, request, view)
        if request.method in permissions.SAFE_METHODS:  #check permission for readonly request(req is get so only accessing data)safe method means get call
            return True
        else:
            return bool(request.user and request.user.is_staff)   #checking user is admin or not
    
class ReviewUserOrReadOnly(permissions.BasePermission):    
    
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:  #check permission for readonly request(req is get so only accessing data)safe method means get call
            return True
        else:
            return obj.review_user == request.user   #checking logedin user is review user or not
            
