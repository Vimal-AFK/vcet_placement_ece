import pandas as pd
from django.contrib import admin, messages
from django.http import HttpResponse , HttpResponseRedirect
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'batch_year', 'section', 'gender', 'average_percentage')
    search_fields = ('username', 'name', 'phone_number', 'section')
    list_filter = ('batch_year', 'gender', 'section')
    actions = ['export_users_to_excel', 'import_users_from_excel']

    def export_users_to_excel(self, request, queryset):
        """Export selected users to an Excel file."""
        if not queryset:
            self.message_user(request, "No users selected.", level=messages.ERROR)
            return

        # Create a pandas DataFrame from the queryset
        data = list(queryset.values('username', 'name', 'batch_year', 'section', 'date_of_birth', 'phone_number', 'gender', 'average_percentage'))
        df = pd.DataFrame(data)

        # Create a response with the Excel file
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=users.xlsx'

        # Save the DataFrame to the response as an Excel file
        df.to_excel(response, index=False, engine='openpyxl')
        return response

    export_users_to_excel.short_description = "Export selected users to Excel"

    def import_users_from_excel(self, request, queryset):
        """Custom admin action to import users from an Excel file."""
        if 'apply' in request.POST:
            excel_file = request.FILES.get('excel_file')
            if not excel_file:
                self.message_user(request, "No file selected.", level=messages.ERROR)
                return HttpResponseRedirect(request.get_full_path())

            try:
                # Read the Excel file using pandas
                df = pd.read_excel(excel_file)

                # Validate required columns
                required_columns = ['username', 'name', 'batch_year', 'section', 'date_of_birth', 'phone_number', 'gender']
                for column in required_columns:
                    if column not in df.columns:
                        raise ValueError(f"Missing column: {column}")

                # Import users from the Excel file
                for _, row in df.iterrows():
                    User.objects.update_or_create(
                        username=row['username'],
                        defaults={
                            'name': row['name'],
                            'batch_year': row['batch_year'],
                            'section': row['section'],
                            'date_of_birth': row['date_of_birth'],
                            'phone_number': row['phone_number'],
                            'gender': row['gender'],
                        }
                    )

                self.message_user(request, "Users imported successfully.", level=messages.SUCCESS)

            except Exception as e:
                self.message_user(request, f"Error importing users: {e}", level=messages.ERROR)

            return HttpResponseRedirect(request.get_full_path())

    import_users_from_excel.short_description = "Import Users from Excel"
