class A:

    def post(self):
        client = "smjdrums@gmail.com"
        A.test = client


class B(A):

    def send_email(self):
        B.output = A.test
        print(B.output)


B().send_email()

A().post()
