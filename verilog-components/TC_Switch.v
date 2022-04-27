module TC_Switch(dis, in, out);
    parameter size = 1;
    input dis;
    input [size-1:0] in;
    tri0 reg [size-1:0] out;
    
    always @ (en or in) begin
        case(en)
        1'b0 : out <= in;
        1'b1 : out <= {size{1'bZ}};
        endcase
    end
endmodule

